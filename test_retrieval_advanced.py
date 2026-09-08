"""Pruebas locales; no descargan modelos ni realizan llamadas a OpenAI."""
import unittest
from types import SimpleNamespace
from unittest.mock import patch
import retrieval_advanced as retrieval


def chunk(key, text):
    return SimpleNamespace(chunk_id=key, text=text, source=key, page=1, section=None)


class RetrievalTests(unittest.TestCase):
    def test_tokenizacion_preserva_codigos_y_acentos(self):
        self.assertEqual(retrieval.tokenize('Error F110-031, cláusula 14.3.'),
                         ['error', 'f110-031', 'cláusula', '14.3'])

    def test_rrf_fusiona_y_no_cuenta_duplicados(self):
        a, b = chunk('a', 'SAP'), chunk('b', 'credenciales')
        result = retrieval.reciprocal_rank_fusion({
            'lexico': [{'chunk': a}, {'chunk': a}, {'chunk': b}],
            'vector': [{'chunk': b}, {'chunk': a}]})
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['chunk'].chunk_id, 'a')
        self.assertAlmostEqual(result[0]['rrf_score'], 1/61 + 1/62)
        self.assertEqual(result[0]['ranks'], {'lexico': 1, 'vector': 2})

    def test_bm25_prioriza_codigo_y_omite_no_coincidentes(self):
        records = [SimpleNamespace(chunk=chunk(str(i), text)) for i, text in enumerate(
            ['Error F110-031 SAP', 'manual de credenciales', 'vacaciones y descanso', 'pagos generales'])]
        with patch.object(retrieval, 'load_store', return_value=SimpleNamespace(records=records)):
            result = retrieval.bm25_search('F110-031')
            self.assertEqual([r['chunk'].chunk_id for r in result], ['0'])
            self.assertEqual(retrieval.bm25_search('inexistente'), [])

    def test_reranker_ordena_sin_perder_trazabilidad(self):
        candidates = [{'chunk': chunk('a', 'uno'), 'rrf_score': .02},
                      {'chunk': chunk('b', 'dos'), 'rrf_score': .01}]
        with patch.object(retrieval, 'load_reranker') as factory:
            factory.return_value.predict.return_value = [.1, .9]
            result = retrieval.rerank('pregunta', candidates, 1)
            self.assertEqual(result[0]['chunk'].chunk_id, 'b')
            self.assertEqual(result[0]['rrf_score'], .01)
            self.assertNotIn('rerank_score', candidates[1])
        with patch.object(retrieval, 'load_reranker') as factory:
            self.assertEqual(retrieval.rerank('pregunta', []), [])
            factory.assert_not_called()

    def test_multi_query_deduplica_sin_destruir_codigo_numerico(self):
        with patch.object(retrieval, 'generate_text', return_value='1. SAP F110-031\n2. SAP F110-031\n123-456 fallo'):
            self.assertEqual(retrieval.generate_queries(None, None, 'fallo'), ['SAP F110-031', '123-456 fallo'])

    def test_pipeline_recorta_candidatos_y_permite_no_reescribir(self):
        candidates = [{'chunk': chunk(str(i), str(i))} for i in range(4)]
        with patch.object(retrieval, 'rewrite_query') as rewrite, \
             patch.object(retrieval, 'bm25_search', return_value=[]), \
             patch.object(retrieval, 'vector_search', return_value=[]), \
             patch.object(retrieval, 'reciprocal_rank_fusion', return_value=candidates), \
             patch.object(retrieval, 'rerank', return_value=[]) as reranker:
            query, result = retrieval.advanced_retrieval(None, None, 'SAP', candidate_k=2, top_k=1, use_rewrite=False)
            rewrite.assert_not_called()
            reranker.assert_called_once_with('SAP', candidates[:2], 1)
            self.assertEqual(query, 'SAP')


if __name__ == '__main__':
    unittest.main()
