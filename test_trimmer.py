"""
Unit tests for the filter_telomeric_reads library
"""

import filter_telomeric_reads


class TestTrimmer:

    def test_reverse_complement_sequence(self):
        assert "AGCT" == filter_telomeric_reads.reverse_complement_sequence(
            "AGCT")

    def test_trim_reverse(self):
        assert "AGTTCTGGTATCTTAGTATTAGCATCTTAGTATTAGCATCTTAGTATTAGCATCTTAGTATTAGC" == filter_telomeric_reads.trim_reverse(
            "GCCTAAGCCTAAGCCTAAGCCTAAAGTTCTGGTATCTTAGTATTAGCATCTTAGTATTAGCATCTTAGTATTAGCATCTTAGTATTAGC", "GCCTAA", 3)
        
    def test_trim_forward(self):
        assert "AGTTCTGGTATCTTAGTATTAGCATCTTAGTATTAGCATCTTAGTATTAGCATCTTAGTATTAGC" == filter_telomeric_reads.trim_forward(
            "GCTAATACTAAGATGCTAATACTAAGATGCTAATACTAAGATGCTAATACTAAGATACCAGAACTTTAGGCTTAGGCTTAGGCTTAGGC", "TTAGGC", 3)
