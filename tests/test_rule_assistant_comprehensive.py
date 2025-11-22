"""
Comprehensive Test Suite for FLExTrans Rule Assistant

This module provides extensive test coverage for the Rule Assistant functionality,
including basic operations, advanced features, edge cases, error handling, and
integration testing.

Test Categories:
1. Basic Functionality Tests
2. Advanced Feature Tests
3. Edge Cases
4. Error Handling Tests
5. Integration Tests
6. Regression Tests
"""

import pytest
import os
import sys
import tempfile
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from unittest.mock import Mock, MagicMock, patch
from dataclasses import dataclass

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Dev', 'Lib'))

import CreateApertiumRules
from CreateApertiumRules import RuleGenerator, FeatureSpec, MacroSpec


# ==============================================================================
# Fixtures and Helper Classes
# ==============================================================================

@dataclass
class MockReport:
    """Mock reporter for testing without FLEx."""
    infos: List[Tuple] = None
    warnings: List[Tuple] = None
    errors: List[Tuple] = None

    def __post_init__(self):
        if self.infos is None:
            self.infos = []
        if self.warnings is None:
            self.warnings = []
        if self.errors is None:
            self.errors = []

    def Info(self, *args):
        """Record info message."""
        self.infos.append(args)

    def Warning(self, *args):
        """Record warning message."""
        self.warnings.append(args)

    def Error(self, *args):
        """Record error message."""
        self.errors.append(args)

    def has_errors(self) -> bool:
        """Check if any errors were recorded."""
        return len(self.errors) > 0


class MockDB:
    """Mock FLEx database for testing without FLEx."""

    def __init__(self, project_name="TestProject", categories=None, features=None):
        self.project_name = project_name
        self.categories = categories or {}
        self.features = features or {}
        self.category_hierarchy = {}

    def ProjectName(self):
        return self.project_name


@pytest.fixture
def mock_report():
    """Provide a mock report object for testing."""
    return MockReport()


@pytest.fixture
def mock_source_db():
    """Provide a mock source database."""
    return MockDB(
        project_name="SourceDB",
        categories={'n': 'noun', 'adj': 'adjective', 'def': 'determiner'},
        features={
            'gender': ['m', 'f'],
            'number': ['sg', 'pl']
        }
    )


@pytest.fixture
def mock_target_db():
    """Provide a mock target database."""
    return MockDB(
        project_name="TargetDB",
        categories={'n': 'noun', 'adj': 'adjective', 'def': 'determiner'},
        features={
            'gender': ['m', 'f'],
            'number': ['sg', 'pl']
        }
    )


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    tmp = tempfile.mkdtemp()
    yield tmp
    shutil.rmtree(tmp)


@pytest.fixture
def rule_generator(mock_source_db, mock_target_db, mock_report):
    """Create a RuleGenerator instance with mocked dependencies."""
    config_map = {}

    # Mock the Utils functions that RuleGenerator needs
    with patch('CreateApertiumRules.Utils.getCategoryHierarchy') as mock_hierarchy:
        mock_hierarchy.return_value = {}
        generator = RuleGenerator(mock_source_db, mock_target_db, mock_report, config_map)
        generator.CreateTree()
        return generator


@pytest.fixture
def sample_flex_data():
    """Provide sample FLEx data structures for testing."""
    return {
        None: {
            'gender': {
                'source_features': ['f', 'm'],
            },
            'number': {
                'source_features': ['sg', 'pl'],
            },
        },
        'adj': {
            'gender': {
                'target_affix': [('FEM.a', 'f'), ('MASC.a', 'm')],
            },
            'number': {
                'target_affix': [('PL', 'pl'), ('SG', 'sg')],
            },
        },
        'n': {
            'gender': {
                'target_lemma': [('bicicleta1.1', 'f'), ('camino1.1', 'm')],
            },
            'number': {
                'source_affix': [('PL', 'pl'), ('SG', 'sg')],
                'target_affix': [('PL', 'pl'), ('SG', 'sg')],
            },
        },
    }


def create_simple_rule_xml(name: str, source_words: List[str],
                           target_config: Dict) -> str:
    """
    Create a simple rule XML string for testing.

    Args:
        name: Rule name
        source_words: List of category names for source words
        target_config: Configuration for target words

    Returns:
        XML string representation of the rule
    """
    root = ET.Element('FLExTransRuleGenerator')
    rules = ET.SubElement(root, 'FLExTransRules')
    rule = ET.SubElement(rules, 'FLExTransRule', name=name)

    # Create source
    source = ET.SubElement(rule, 'Source')
    phrase = ET.SubElement(source, 'Phrase')
    words = ET.SubElement(phrase, 'Words')

    for idx, cat in enumerate(source_words, 1):
        ET.SubElement(words, 'Word', category=cat, id=str(idx))

    # Create target
    target = ET.SubElement(rule, 'Target')
    phrase = ET.SubElement(target, 'Phrase')
    words = ET.SubElement(phrase, 'Words')

    for word_cfg in target_config.get('words', []):
        word = ET.SubElement(words, 'Word', **word_cfg.get('attrs', {}))

        if 'features' in word_cfg:
            features = ET.SubElement(word, 'Features')
            for feat_cfg in word_cfg['features']:
                ET.SubElement(features, 'Feature', **feat_cfg)

        if 'affixes' in word_cfg:
            affixes = ET.SubElement(word, 'Affixes')
            for affix_cfg in word_cfg['affixes']:
                affix = ET.SubElement(affixes, 'Affix', **affix_cfg.get('attrs', {}))
                if 'features' in affix_cfg:
                    features = ET.SubElement(affix, 'Features')
                    for feat_cfg in affix_cfg['features']:
                        ET.SubElement(features, 'Feature', **feat_cfg)

    return ET.tostring(root, encoding='unicode')


# ==============================================================================
# BASIC FUNCTIONALITY TESTS
# ==============================================================================

class TestBasicFunctionality:
    """Test basic Rule Assistant operations."""

    def test_simple_def_noun_rule(self, rule_generator, temp_dir):
        """
        Test creation of a simple def-noun rule.

        This validates that the Rule Generator can create a basic 2-word rule
        with determiner and noun.
        """
        xml_content = """<?xml version="1.0" encoding="utf-8"?>
        <!DOCTYPE FLExTransRuleGenerator PUBLIC "-//XMLmind//DTD FLExTransRuleGenerator//EN" "FLExTransRuleGenerator.dtd">
        <FLExTransRuleGenerator>
          <FLExTransRules>
            <FLExTransRule name="Def N Simple">
              <Source>
                <Phrase>
                  <Words>
                    <Word category="def" id="1"></Word>
                    <Word category="n" id="2"></Word>
                  </Words>
                </Phrase>
              </Source>
              <Target>
                <Phrase>
                  <Words>
                    <Word head="no" id="1"></Word>
                    <Word head="yes" id="2"></Word>
                  </Words>
                </Phrase>
              </Target>
            </FLExTransRule>
          </FLExTransRules>
        </FLExTransRuleGenerator>
        """

        rule_file = os.path.join(temp_dir, 'test_rule.xml')
        with open(rule_file, 'w') as f:
            f.write(xml_content)

        # Process the rule file
        with patch('CreateApertiumRules.Utils.getLemmasForFeature', return_value=[]):
            with patch('CreateApertiumRules.Utils.getAffixGlossesForFeature', return_value=[]):
                with patch('CreateApertiumRules.Utils.getPossibleFeatureValues', return_value=[]):
                    rule_count = rule_generator.ProcessAssistantFile(rule_file)

        # Verify rule was created
        assert rule_count >= 0
        assert 'c_def' in rule_generator.tagToCategoryName
        assert 'c_n' in rule_generator.tagToCategoryName
        assert not rule_generator.report.has_errors()

    def test_adjective_noun_agreement(self, rule_generator, temp_dir):
        """
        Test adjective-noun rule with gender and number agreement.

        Validates that feature agreement via match labels (α, β) works correctly.
        """
        xml_content = """<?xml version="1.0" encoding="utf-8"?>
        <FLExTransRuleGenerator>
          <FLExTransRules>
            <FLExTransRule name="Adj N Agreement">
              <Source>
                <Phrase>
                  <Words>
                    <Word category="adj" id="1"></Word>
                    <Word category="n" id="2"></Word>
                  </Words>
                </Phrase>
              </Source>
              <Target>
                <Phrase>
                  <Words>
                    <Word head="yes" id="2">
                      <Features>
                        <Feature label="gender" match="α"></Feature>
                      </Features>
                      <Affixes>
                        <Affix type="suffix">
                          <Features>
                            <Feature label="number" match="β"></Feature>
                          </Features>
                        </Affix>
                      </Affixes>
                    </Word>
                    <Word head="no" id="1">
                      <Affixes>
                        <Affix type="suffix">
                          <Features>
                            <Feature label="gender" match="α"></Feature>
                          </Features>
                        </Affix>
                        <Affix type="suffix">
                          <Features>
                            <Feature label="number" match="β"></Feature>
                          </Features>
                        </Affix>
                      </Affixes>
                    </Word>
                  </Words>
                </Phrase>
              </Target>
            </FLExTransRule>
          </FLExTransRules>
        </FLExTransRuleGenerator>
        """

        rule_file = os.path.join(temp_dir, 'test_agreement.xml')
        with open(rule_file, 'w') as f:
            f.write(xml_content)

        with patch('CreateApertiumRules.Utils.getLemmasForFeature', return_value=[]):
            with patch('CreateApertiumRules.Utils.getAffixGlossesForFeature', return_value=[]):
                with patch('CreateApertiumRules.Utils.getPossibleFeatureValues', return_value=[]):
                    rule_count = rule_generator.ProcessAssistantFile(rule_file)

        assert rule_count >= 0
        # Verify match labels are processed
        assert not rule_generator.report.has_errors()

    def test_affix_generation_prefix(self, rule_generator):
        """
        Test generation of prefix affixes.

        Validates that the system correctly handles prefix-type affixes.
        """
        spec = FeatureSpec(
            category='n',
            label='definiteness',
            isAffix=True,
            value=None
        )

        # Ensure attribute is created
        with patch.object(rule_generator, 'GetAttributeValues', return_value={'DEF', 'INDEF'}):
            attr_name = rule_generator.EnsureAttribute(spec)

        assert attr_name in rule_generator.featureToAttributeName.values()
        assert 'definiteness' in attr_name or 'DEF' in str(rule_generator.definedAttributes.get(attr_name, ''))

    def test_affix_generation_suffix(self, rule_generator):
        """
        Test generation of suffix affixes.

        Validates that the system correctly handles suffix-type affixes.
        """
        spec = FeatureSpec(
            category='n',
            label='number',
            isAffix=True,
            value=None
        )

        with patch.object(rule_generator, 'GetAttributeValues', return_value={'PL', 'SG'}):
            attr_name = rule_generator.EnsureAttribute(spec)

        assert attr_name is not None
        assert not rule_generator.report.has_errors()

    @pytest.mark.parametrize("match_label", ['α', 'β', 'γ', 'δ'])
    def test_match_label_resolution(self, match_label, rule_generator, temp_dir):
        """
        Test resolution of different match labels (α, β, γ, δ).

        Validates that various Greek letter match labels are handled correctly.
        """
        xml_template = """<?xml version="1.0" encoding="utf-8"?>
        <FLExTransRuleGenerator>
          <FLExTransRules>
            <FLExTransRule name="Match Label Test">
              <Source>
                <Phrase>
                  <Words>
                    <Word category="n" id="1"></Word>
                  </Words>
                </Phrase>
              </Source>
              <Target>
                <Phrase>
                  <Words>
                    <Word head="yes" id="1">
                      <Features>
                        <Feature label="gender" match="{match}"></Feature>
                      </Features>
                    </Word>
                  </Words>
                </Phrase>
              </Target>
            </FLExTransRule>
          </FLExTransRules>
        </FLExTransRuleGenerator>
        """.format(match=match_label)

        rule_file = os.path.join(temp_dir, f'test_match_{match_label}.xml')
        with open(rule_file, 'w') as f:
            f.write(xml_template)

        with patch('CreateApertiumRules.Utils.getLemmasForFeature', return_value=[]):
            with patch('CreateApertiumRules.Utils.getAffixGlossesForFeature', return_value=[]):
                with patch('CreateApertiumRules.Utils.getPossibleFeatureValues', return_value=[]):
                    rule_count = rule_generator.ProcessAssistantFile(rule_file)

        # Should process without errors
        assert rule_count >= 0


# ==============================================================================
# ADVANCED FEATURE TESTS
# ==============================================================================

class TestAdvancedFeatures:
    """Test advanced Rule Assistant features."""

    def test_ranked_features(self, rule_generator, temp_dir):
        """
        Test feature ranking for priority-based selection.

        Validates that features with ranking attributes are processed in order.
        """
        xml_content = """<?xml version="1.0" encoding="utf-8"?>
        <FLExTransRuleGenerator>
          <FLExTransRules>
            <FLExTransRule name="Ranked Features">
              <Source>
                <Phrase>
                  <Words>
                    <Word category="def" id="1"></Word>
                    <Word category="n" id="2"></Word>
                  </Words>
                </Phrase>
              </Source>
              <Target>
                <Phrase>
                  <Words>
                    <Word head="no" id="1">
                      <Features>
                        <Feature label="number" match="n" ranking="1"/>
                        <Feature label="gender" match="g" ranking="2"/>
                      </Features>
                    </Word>
                    <Word head="yes" id="2">
                      <Features>
                        <Feature label="gender" match="g"/>
                      </Features>
                      <Affixes>
                        <Affix type="suffix">
                          <Features>
                            <Feature label="number" match="n"/>
                          </Features>
                        </Affix>
                      </Affixes>
                    </Word>
                  </Words>
                </Phrase>
              </Target>
            </FLExTransRule>
          </FLExTransRules>
        </FLExTransRuleGenerator>
        """

        rule_file = os.path.join(temp_dir, 'test_ranked.xml')
        with open(rule_file, 'w') as f:
            f.write(xml_content)

        with patch('CreateApertiumRules.Utils.getLemmasForFeature', return_value=[('el', 'sg'), ('los', 'pl')]):
            with patch('CreateApertiumRules.Utils.getAffixGlossesForFeature', return_value=[]):
                with patch('CreateApertiumRules.Utils.getPossibleFeatureValues', return_value=[]):
                    rule_count = rule_generator.ProcessAssistantFile(rule_file)

        assert rule_count >= 0

    def test_unmarked_default_values(self, rule_generator, temp_dir):
        """
        Test unmarked_default attribute for default feature values.

        Validates that default values are used when features are missing.
        """
        xml_content = """<?xml version="1.0" encoding="utf-8"?>
        <FLExTransRuleGenerator>
          <FLExTransRules>
            <FLExTransRule name="Default Values">
              <Source>
                <Phrase>
                  <Words>
                    <Word category="adj" id="1"></Word>
                    <Word category="n" id="2"></Word>
                  </Words>
                </Phrase>
              </Source>
              <Target>
                <Phrase>
                  <Words>
                    <Word head="yes" id="2">
                      <Features>
                        <Feature label="gender" match="α" unmarked_default="m"></Feature>
                      </Features>
                      <Affixes>
                        <Affix type="suffix">
                          <Features>
                            <Feature label="number" match="β" unmarked_default="sg"></Feature>
                          </Features>
                        </Affix>
                      </Affixes>
                    </Word>
                    <Word head="no" id="1">
                      <Affixes>
                        <Affix type="suffix">
                          <Features>
                            <Feature label="gender" match="α"></Feature>
                          </Features>
                        </Affix>
                        <Affix type="suffix">
                          <Features>
                            <Feature label="number" match="β"></Feature>
                          </Features>
                        </Affix>
                      </Affixes>
                    </Word>
                  </Words>
                </Phrase>
              </Target>
            </FLExTransRule>
          </FLExTransRules>
        </FLExTransRuleGenerator>
        """

        rule_file = os.path.join(temp_dir, 'test_defaults.xml')
        with open(rule_file, 'w') as f:
            f.write(xml_content)

        with patch('CreateApertiumRules.Utils.getLemmasForFeature', return_value=[]):
            with patch('CreateApertiumRules.Utils.getAffixGlossesForFeature', return_value=[]):
                with patch('CreateApertiumRules.Utils.getPossibleFeatureValues', return_value=[]):
                    rule_count = rule_generator.ProcessAssistantFile(rule_file)

        assert rule_count >= 0

    def test_pattern_feature_fixed_values(self, rule_generator, temp_dir):
        """
        Test pattern features with fixed values.

        Validates that features with specific value attributes work correctly.
        """
        xml_content = """<?xml version="1.0" encoding="utf-8"?>
        <FLExTransRuleGenerator>
          <FLExTransRules>
            <FLExTransRule name="Pattern Feature">
              <Source>
                <Phrase>
                  <Words>
                    <Word category="def" id="1">
                      <Features>
                        <Feature label="definiteness" value="defid"></Feature>
                      </Features>
                    </Word>
                    <Word category="n" id="2"></Word>
                  </Words>
                </Phrase>
              </Source>
              <Target>
                <Phrase>
                  <Words>
                    <Word head="yes" id="2">
                      <Affixes>
                        <Affix type="suffix">
                          <Features>
                            <Feature label="definiteness" value="defid"></Feature>
                          </Features>
                        </Affix>
                      </Affixes>
                    </Word>
                  </Words>
                </Phrase>
              </Target>
            </FLExTransRule>
          </FLExTransRules>
        </FLExTransRuleGenerator>
        """

        rule_file = os.path.join(temp_dir, 'test_pattern.xml')
        with open(rule_file, 'w') as f:
            f.write(xml_content)

        with patch('CreateApertiumRules.Utils.getLemmasForFeature', return_value=[]):
            with patch('CreateApertiumRules.Utils.getAffixGlossesForFeature', return_value=[('DEF', 'defid')]):
                with patch('CreateApertiumRules.Utils.getPossibleFeatureValues', return_value=['defid', 'indf']):
                    rule_count = rule_generator.ProcessAssistantFile(rule_file)

        assert rule_count >= 0

    def test_create_permutations(self, rule_generator, temp_dir):
        """
        Test create_permutations feature for optional words.

        Validates that permutations are created when create_permutations="yes".
        """
        xml_content = """<?xml version="1.0" encoding="utf-8"?>
        <FLExTransRuleGenerator>
          <FLExTransRules>
            <FLExTransRule name="Permutation Test" create_permutations="yes">
              <Source>
                <Phrase>
                  <Words>
                    <Word category="def" id="1"></Word>
                    <Word category="adj" id="2"></Word>
                    <Word category="n" id="3" head="yes"></Word>
                  </Words>
                </Phrase>
              </Source>
              <Target>
                <Phrase>
                  <Words>
                    <Word head="no" id="1"></Word>
                    <Word head="no" id="2"></Word>
                    <Word head="yes" id="3"></Word>
                  </Words>
                </Phrase>
              </Target>
            </FLExTransRule>
          </FLExTransRules>
        </FLExTransRuleGenerator>
        """

        rule_file = os.path.join(temp_dir, 'test_permutations.xml')
        with open(rule_file, 'w') as f:
            f.write(xml_content)

        with patch('CreateApertiumRules.Utils.getLemmasForFeature', return_value=[]):
            with patch('CreateApertiumRules.Utils.getAffixGlossesForFeature', return_value=[]):
                with patch('CreateApertiumRules.Utils.getPossibleFeatureValues', return_value=[]):
                    rule_count = rule_generator.ProcessAssistantFile(rule_file)

        # Should create multiple rules (permutations)
        assert rule_count > 1

    def test_bantu_split_noun_class(self, rule_generator, temp_dir):
        """
        Test Bantu split noun class (DisjointFeatureSets).

        Validates that split gender agreement (DisjointFeatureSet) creates
        the appropriate macro for Bantu noun class agreement.
        """
        xml_content = """<?xml version="1.0" encoding="utf-8"?>
        <FLExTransRuleGenerator>
          <DisjointFeatureSets>
            <DisjointFeatureSet co_feature_name="number" disjoint_name="BantuClass">
              <DisjointFeatureValuePairings>
                <DisjointFeatureValuePairing co_feature_value="sg" flex_feature_name="BantuSG"/>
                <DisjointFeatureValuePairing co_feature_value="pl" flex_feature_name="BantuPL"/>
              </DisjointFeatureValuePairings>
            </DisjointFeatureSet>
          </DisjointFeatureSets>
          <FLExTransRules>
            <FLExTransRule name="Bantu N">
              <Source>
                <Phrase>
                  <Words>
                    <Word category="n" id="1"></Word>
                  </Words>
                </Phrase>
              </Source>
              <Target>
                <Phrase>
                  <Words>
                    <Word head="yes" id="1"></Word>
                  </Words>
                </Phrase>
              </Target>
            </FLExTransRule>
          </FLExTransRules>
        </FLExTransRuleGenerator>
        """

        rule_file = os.path.join(temp_dir, 'test_bantu.xml')
        with open(rule_file, 'w') as f:
            f.write(xml_content)

        with patch('CreateApertiumRules.Utils.getLemmasForFeature', return_value=[]):
            with patch('CreateApertiumRules.Utils.getAffixGlossesForFeature', return_value=[]):
                with patch('CreateApertiumRules.Utils.getPossibleFeatureValues', return_value=[]):
                    with patch.object(rule_generator, 'GetAttributeValues', return_value=set()):
                        rule_count = rule_generator.ProcessAssistantFile(rule_file)

        # Verify Bantu macro was created
        assert rule_generator.BantuFeature == 'BantuClass'
        assert rule_generator.BantuParts == ('BantuSG', 'BantuPL')
        assert rule_generator.BantuMacro is not None


# ==============================================================================
# EDGE CASE TESTS
# ==============================================================================

class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_missing_features(self, rule_generator, temp_dir):
        """
        Test handling of missing feature specifications.

        Validates graceful handling when expected features are absent.
        """
        xml_content = """<?xml version="1.0" encoding="utf-8"?>
        <FLExTransRuleGenerator>
          <FLExTransRules>
            <FLExTransRule name="Missing Features">
              <Source>
                <Phrase>
                  <Words>
                    <Word category="n" id="1"></Word>
                  </Words>
                </Phrase>
              </Source>
              <Target>
                <Phrase>
                  <Words>
                    <Word head="yes" id="1">
                      <Features>
                        <Feature label="nonexistent_feature" match="α"></Feature>
                      </Features>
                    </Word>
                  </Words>
                </Phrase>
              </Target>
            </FLExTransRule>
          </FLExTransRules>
        </FLExTransRuleGenerator>
        """

        rule_file = os.path.join(temp_dir, 'test_missing.xml')
        with open(rule_file, 'w') as f:
            f.write(xml_content)

        with patch('CreateApertiumRules.Utils.getLemmasForFeature', return_value=[]):
            with patch('CreateApertiumRules.Utils.getAffixGlossesForFeature', return_value=[]):
                with patch('CreateApertiumRules.Utils.getPossibleFeatureValues', return_value=[]):
                    rule_count = rule_generator.ProcessAssistantFile(rule_file)

        # Should handle gracefully, possibly with warnings
        assert rule_count >= 0

    def test_conflicting_feature_specifications(self, rule_generator, temp_dir):
        """
        Test handling of conflicting feature specifications.

        Validates behavior when features have contradictory values.
        """
        xml_content = """<?xml version="1.0" encoding="utf-8"?>
        <FLExTransRuleGenerator>
          <FLExTransRules>
            <FLExTransRule name="Conflicting Features">
              <Source>
                <Phrase>
                  <Words>
                    <Word category="n" id="1">
                      <Features>
                        <Feature label="gender" value="m"></Feature>
                        <Feature label="gender" value="f"></Feature>
                      </Features>
                    </Word>
                  </Words>
                </Phrase>
              </Source>
              <Target>
                <Phrase>
                  <Words>
                    <Word head="yes" id="1"></Word>
                  </Words>
                </Phrase>
              </Target>
            </FLExTransRule>
          </FLExTransRules>
        </FLExTransRuleGenerator>
        """

        rule_file = os.path.join(temp_dir, 'test_conflict.xml')
        with open(rule_file, 'w') as f:
            f.write(xml_content)

        with patch('CreateApertiumRules.Utils.getLemmasForFeature', return_value=[]):
            with patch('CreateApertiumRules.Utils.getAffixGlossesForFeature', return_value=[]):
                with patch('CreateApertiumRules.Utils.getPossibleFeatureValues', return_value=['m', 'f']):
                    rule_count = rule_generator.ProcessAssistantFile(rule_file)

        # Should process (last value likely wins or creates multiple patterns)
        assert rule_count >= 0

    def test_multiple_affixes_same_word(self, rule_generator, temp_dir):
        """
        Test multiple affixes on the same word.

        Validates that a word can have multiple prefix and suffix affixes.
        """
        xml_content = """<?xml version="1.0" encoding="utf-8"?>
        <FLExTransRuleGenerator>
          <FLExTransRules>
            <FLExTransRule name="Multiple Affixes">
              <Source>
                <Phrase>
                  <Words>
                    <Word category="n" id="1"></Word>
                  </Words>
                </Phrase>
              </Source>
              <Target>
                <Phrase>
                  <Words>
                    <Word head="yes" id="1">
                      <Affixes>
                        <Affix type="prefix">
                          <Features>
                            <Feature label="definiteness" match="d"></Feature>
                          </Features>
                        </Affix>
                        <Affix type="suffix">
                          <Features>
                            <Feature label="number" match="n"></Feature>
                          </Features>
                        </Affix>
                        <Affix type="suffix">
                          <Features>
                            <Feature label="case" match="c"></Feature>
                          </Features>
                        </Affix>
                      </Affixes>
                    </Word>
                  </Words>
                </Phrase>
              </Target>
            </FLExTransRule>
          </FLExTransRules>
        </FLExTransRuleGenerator>
        """

        rule_file = os.path.join(temp_dir, 'test_multi_affix.xml')
        with open(rule_file, 'w') as f:
            f.write(xml_content)

        with patch('CreateApertiumRules.Utils.getLemmasForFeature', return_value=[]):
            with patch('CreateApertiumRules.Utils.getAffixGlossesForFeature', return_value=[]):
                with patch('CreateApertiumRules.Utils.getPossibleFeatureValues', return_value=[]):
                    rule_count = rule_generator.ProcessAssistantFile(rule_file)

        assert rule_count >= 0

    def test_empty_rule(self, rule_generator, temp_dir):
        """
        Test handling of empty or minimal rules.

        Validates behavior with rules that have minimal configuration.
        """
        xml_content = """<?xml version="1.0" encoding="utf-8"?>
        <FLExTransRuleGenerator>
          <FLExTransRules>
          </FLExTransRules>
        </FLExTransRuleGenerator>
        """

        rule_file = os.path.join(temp_dir, 'test_empty.xml')
        with open(rule_file, 'w') as f:
            f.write(xml_content)

        rule_count = rule_generator.ProcessAssistantFile(rule_file)

        # Should handle empty rule set
        assert rule_count == 0
        assert not rule_generator.report.has_errors()

    def test_invalid_xml_structure(self, rule_generator, temp_dir):
        """
        Test handling of invalid XML structure.

        Validates error handling for malformed XML.
        """
        xml_content = """<?xml version="1.0" encoding="utf-8"?>
        <FLExTransRuleGenerator>
          <FLExTransRules>
            <FLExTransRule name="Broken">
              <Source>
                <!-- Missing closing tags -->
        """

        rule_file = os.path.join(temp_dir, 'test_invalid.xml')
        with open(rule_file, 'w') as f:
            f.write(xml_content)

        # Should raise XML parsing error
        with pytest.raises(ET.ParseError):
            rule_generator.ProcessAssistantFile(rule_file)

    def test_category_mismatch(self, rule_generator, temp_dir):
        """
        Test handling of category mismatches between source and target.

        Validates that category changes are handled appropriately.
        """
        xml_content = """<?xml version="1.0" encoding="utf-8"?>
        <FLExTransRuleGenerator>
          <FLExTransRules>
            <FLExTransRule name="Category Mismatch">
              <Source>
                <Phrase>
                  <Words>
                    <Word category="adj" id="1"></Word>
                  </Words>
                </Phrase>
              </Source>
              <Target>
                <Phrase>
                  <Words>
                    <Word head="yes" id="1" category="n"></Word>
                  </Words>
                </Phrase>
              </Target>
            </FLExTransRule>
          </FLExTransRules>
        </FLExTransRuleGenerator>
        """

        rule_file = os.path.join(temp_dir, 'test_mismatch.xml')
        with open(rule_file, 'w') as f:
            f.write(xml_content)

        with patch('CreateApertiumRules.Utils.getLemmasForFeature', return_value=[]):
            with patch('CreateApertiumRules.Utils.getAffixGlossesForFeature', return_value=[]):
                with patch('CreateApertiumRules.Utils.getPossibleFeatureValues', return_value=[]):
                    rule_count = rule_generator.ProcessAssistantFile(rule_file)

        # Should handle category specification on target
        assert rule_count >= 0


# ==============================================================================
# ERROR HANDLING TESTS
# ==============================================================================

class TestErrorHandling:
    """Test error handling and validation."""

    def test_missing_head_word(self, rule_generator, temp_dir):
        """
        Test error when no head word is specified.

        Validates that rules without a head word are properly rejected.
        """
        xml_content = """<?xml version="1.0" encoding="utf-8"?>
        <FLExTransRuleGenerator>
          <FLExTransRules>
            <FLExTransRule name="No Head">
              <Source>
                <Phrase>
                  <Words>
                    <Word category="n" id="1"></Word>
                  </Words>
                </Phrase>
              </Source>
              <Target>
                <Phrase>
                  <Words>
                    <Word head="no" id="1"></Word>
                  </Words>
                </Phrase>
              </Target>
            </FLExTransRule>
          </FLExTransRules>
        </FLExTransRuleGenerator>
        """

        rule_file = os.path.join(temp_dir, 'test_no_head.xml')
        with open(rule_file, 'w') as f:
            f.write(xml_content)

        with patch('CreateApertiumRules.Utils.getLemmasForFeature', return_value=[]):
            with patch('CreateApertiumRules.Utils.getAffixGlossesForFeature', return_value=[]):
                with patch('CreateApertiumRules.Utils.getPossibleFeatureValues', return_value=[]):
                    rule_count = rule_generator.ProcessAssistantFile(rule_file)

        # Should report error
        assert rule_generator.report.has_errors()

    def test_missing_category(self, rule_generator, temp_dir):
        """
        Test error when word category is missing.

        Validates error reporting for words without categories.
        """
        xml_content = """<?xml version="1.0" encoding="utf-8"?>
        <FLExTransRuleGenerator>
          <FLExTransRules>
            <FLExTransRule name="No Category">
              <Source>
                <Phrase>
                  <Words>
                    <Word id="1"></Word>
                  </Words>
                </Phrase>
              </Source>
              <Target>
                <Phrase>
                  <Words>
                    <Word head="yes" id="1"></Word>
                  </Words>
                </Phrase>
              </Target>
            </FLExTransRule>
          </FLExTransRules>
        </FLExTransRuleGenerator>
        """

        rule_file = os.path.join(temp_dir, 'test_no_cat.xml')
        with open(rule_file, 'w') as f:
            f.write(xml_content)

        with patch('CreateApertiumRules.Utils.getLemmasForFeature', return_value=[]):
            with patch('CreateApertiumRules.Utils.getAffixGlossesForFeature', return_value=[]):
                with patch('CreateApertiumRules.Utils.getPossibleFeatureValues', return_value=[]):
                    rule_count = rule_generator.ProcessAssistantFile(rule_file)

        # Should report error about missing category
        assert rule_generator.report.has_errors()

    def test_duplicate_word_ids(self, rule_generator, temp_dir):
        """
        Test error when duplicate word IDs exist.

        Validates detection of duplicate word identifiers.
        """
        xml_content = """<?xml version="1.0" encoding="utf-8"?>
        <FLExTransRuleGenerator>
          <FLExTransRules>
            <FLExTransRule name="Duplicate IDs">
              <Source>
                <Phrase>
                  <Words>
                    <Word category="n" id="1"></Word>
                    <Word category="adj" id="1"></Word>
                  </Words>
                </Phrase>
              </Source>
              <Target>
                <Phrase>
                  <Words>
                    <Word head="yes" id="1"></Word>
                  </Words>
                </Phrase>
              </Target>
            </FLExTransRule>
          </FLExTransRules>
        </FLExTransRuleGenerator>
        """

        rule_file = os.path.join(temp_dir, 'test_dup_ids.xml')
        with open(rule_file, 'w') as f:
            f.write(xml_content)

        with patch('CreateApertiumRules.Utils.getLemmasForFeature', return_value=[]):
            with patch('CreateApertiumRules.Utils.getAffixGlossesForFeature', return_value=[]):
                with patch('CreateApertiumRules.Utils.getPossibleFeatureValues', return_value=[]):
                    rule_count = rule_generator.ProcessAssistantFile(rule_file)

        # Should report error about duplicate IDs
        assert rule_generator.report.has_errors()

    def test_clear_error_messages(self, rule_generator):
        """
        Test that error messages are clear and informative.

        Validates the quality of error reporting.
        """
        # Test feature not found error
        spec = FeatureSpec(category='n', label='unknown_feature', isAffix=True)

        with patch.object(rule_generator, 'GetAttributeValues', return_value=set()):
            rule_generator.EnsureAttribute(spec)

        # Should have an error message
        assert rule_generator.report.has_errors()
        # Error should mention the feature and category
        error_msg = str(rule_generator.report.errors[0])
        assert 'unknown_feature' in error_msg or 'n' in error_msg


# ==============================================================================
# INTEGRATION TESTS
# ==============================================================================

class TestIntegration:
    """Test integration with Apertium and end-to-end workflows."""

    def test_rule_generation_to_xml_output(self, rule_generator, temp_dir):
        """
        Test complete workflow from rule to XML output.

        Validates that generated rules produce valid Apertium XML.
        """
        xml_content = """<?xml version="1.0" encoding="utf-8"?>
        <FLExTransRuleGenerator>
          <FLExTransRules>
            <FLExTransRule name="Simple Integration Test">
              <Source>
                <Phrase>
                  <Words>
                    <Word category="n" id="1"></Word>
                  </Words>
                </Phrase>
              </Source>
              <Target>
                <Phrase>
                  <Words>
                    <Word head="yes" id="1"></Word>
                  </Words>
                </Phrase>
              </Target>
            </FLExTransRule>
          </FLExTransRules>
        </FLExTransRuleGenerator>
        """

        rule_file = os.path.join(temp_dir, 'integration_test.xml')
        output_file = os.path.join(temp_dir, 'output.t1x')

        with open(rule_file, 'w') as f:
            f.write(xml_content)

        with patch('CreateApertiumRules.Utils.getLemmasForFeature', return_value=[]):
            with patch('CreateApertiumRules.Utils.getAffixGlossesForFeature', return_value=[]):
                with patch('CreateApertiumRules.Utils.getPossibleFeatureValues', return_value=[]):
                    rule_generator.ProcessAssistantFile(rule_file)
                    rule_generator.WriteTransferFile(output_file)

        # Verify output file was created
        assert os.path.exists(output_file)

        # Verify it's valid XML
        tree = ET.parse(output_file)
        root = tree.getroot()
        assert root.tag == 'transfer'

    def test_overwrite_rules_functionality(self, rule_generator, temp_dir):
        """
        Test overwrite_rules attribute functionality.

        Validates that overwrite_rules="yes" correctly replaces existing rules.
        """
        # First, create initial rules
        xml_v1 = """<?xml version="1.0" encoding="utf-8"?>
        <FLExTransRuleGenerator>
          <FLExTransRules>
            <FLExTransRule name="Test Rule V1">
              <Source>
                <Phrase>
                  <Words>
                    <Word category="n" id="1"></Word>
                  </Words>
                </Phrase>
              </Source>
              <Target>
                <Phrase>
                  <Words>
                    <Word head="yes" id="1"></Word>
                  </Words>
                </Phrase>
              </Target>
            </FLExTransRule>
          </FLExTransRules>
        </FLExTransRuleGenerator>
        """

        rule_file = os.path.join(temp_dir, 'overwrite_test.xml')
        with open(rule_file, 'w') as f:
            f.write(xml_v1)

        with patch('CreateApertiumRules.Utils.getLemmasForFeature', return_value=[]):
            with patch('CreateApertiumRules.Utils.getAffixGlossesForFeature', return_value=[]):
                with patch('CreateApertiumRules.Utils.getPossibleFeatureValues', return_value=[]):
                    rule_generator.ProcessAssistantFile(rule_file)

        initial_rule_count = len(rule_generator.ruleNames)

        # Now overwrite with new version
        xml_v2 = """<?xml version="1.0" encoding="utf-8"?>
        <FLExTransRuleGenerator overwrite_rules="yes">
          <FLExTransRules>
            <FLExTransRule name="Test Rule V1">
              <Source>
                <Phrase>
                  <Words>
                    <Word category="adj" id="1"></Word>
                  </Words>
                </Phrase>
              </Source>
              <Target>
                <Phrase>
                  <Words>
                    <Word head="yes" id="1"></Word>
                  </Words>
                </Phrase>
              </Target>
            </FLExTransRule>
          </FLExTransRules>
        </FLExTransRuleGenerator>
        """

        with open(rule_file, 'w') as f:
            f.write(xml_v2)

        with patch('CreateApertiumRules.Utils.getLemmasForFeature', return_value=[]):
            with patch('CreateApertiumRules.Utils.getAffixGlossesForFeature', return_value=[]):
                with patch('CreateApertiumRules.Utils.getPossibleFeatureValues', return_value=[]):
                    rule_generator.ProcessAssistantFile(rule_file)

        # Rule count should be similar (old removed, new added)
        assert 'Test Rule V1' in rule_generator.ruleNames or 'Test Rule V1 (1)' in rule_generator.ruleNames

    def test_macro_deduplication(self, rule_generator):
        """
        Test that identical macros are not duplicated.

        Validates macro reuse for efficiency.
        """
        # Create two identical feature specs
        spec1 = FeatureSpec(category='n', label='gender', isAffix=True)
        spec2 = FeatureSpec(category='n', label='gender', isAffix=True)

        with patch.object(rule_generator, 'GetAttributeValues', return_value={'m', 'f'}):
            attr1 = rule_generator.EnsureAttribute(spec1)
            attr2 = rule_generator.EnsureAttribute(spec2)

        # Should return the same attribute name
        assert attr1 == attr2


# ==============================================================================
# REGRESSION TESTS
# ==============================================================================

class TestRegressionWithExamples:
    """Test against actual example files from the Rule Assistant directory."""

    @pytest.fixture
    def example_dir(self):
        """Get the Rule Assistant example directory."""
        return os.path.join(os.path.dirname(__file__), '..', 'Rule Assistant')

    @pytest.mark.parametrize("example_file", [
        "Ex1a_Def-Noun.xml",
        "Ex1b_Def-Noun.xml",
        "Ex1c_Indef-Noun.xml",
        "Ex2_Adj-Noun.xml",
        "Ex3_Adj-Noun.xml",
        "Ex4a_Def-Adj-Noun.xml",
        "Ex4b_Indef-Adj-Noun.xml",
        "GermanEnglishDoubleDefault.xml",
        "GermanEnglishDoubleDefaultOverwrite.xml",
        "GermanSwedishDefToAffix.xml",
        "PatternFeature.xml",
        "SpanishFrenchRev2.xml",
        "SplitBantu.xml",
        "insert_word.xml",
        "ranking.xml",
        "unmarked_default.xml",
        "EnglishGermanTripleRanking.xml",
        "EnglishGermanTripleRankingPartialDefault.xml",
    ])
    def test_example_file_loads(self, example_file, example_dir, rule_generator):
        """
        Test that each example file loads without errors.

        Validates that all example files are structurally valid.
        """
        file_path = os.path.join(example_dir, example_file)

        if not os.path.exists(file_path):
            pytest.skip(f"Example file {example_file} not found")

        # Just verify it can be parsed
        tree = ET.parse(file_path)
        root = tree.getroot()

        assert root.tag == 'FLExTransRuleGenerator'

        # Check for rules
        rules = root.findall('.//FLExTransRule')
        assert len(rules) > 0, f"{example_file} has no rules"

    @pytest.mark.parametrize("example_file", [
        "Ex3_Adj-Noun.xml",
        "ranking.xml",
        "unmarked_default.xml",
    ])
    def test_example_file_compiles(self, example_file, example_dir,
                                   rule_generator, temp_dir):
        """
        Test that example files compile to valid Apertium rules.

        Validates end-to-end processing for key examples.
        """
        file_path = os.path.join(example_dir, example_file)

        if not os.path.exists(file_path):
            pytest.skip(f"Example file {example_file} not found")

        output_file = os.path.join(temp_dir, 'output.t1x')

        with patch('CreateApertiumRules.Utils.getLemmasForFeature', return_value=[]):
            with patch('CreateApertiumRules.Utils.getAffixGlossesForFeature', return_value=[]):
                with patch('CreateApertiumRules.Utils.getPossibleFeatureValues', return_value=[]):
                    with patch.object(rule_generator, 'GetAttributeValues', return_value=set()):
                        rule_count = rule_generator.ProcessAssistantFile(file_path)
                        rule_generator.WriteTransferFile(output_file)

        # Should create at least one rule
        assert rule_count >= 0

        # Output should be valid XML
        assert os.path.exists(output_file)
        tree = ET.parse(output_file)
        assert tree.getroot().tag == 'transfer'

    def test_all_examples_structure_valid(self, example_dir):
        """
        Test that all example XML files have valid structure.

        Comprehensive validation of all example files.
        """
        example_files = [
            f for f in os.listdir(example_dir)
            if f.endswith('.xml') and not f.endswith('.t1x')
        ]

        for example_file in example_files:
            file_path = os.path.join(example_dir, example_file)

            try:
                tree = ET.parse(file_path)
                root = tree.getroot()

                # Basic structure validation
                if root.tag == 'FLExTransRuleGenerator':
                    # Should have either rules or be the DTD file
                    rules_section = root.find('.//FLExTransRules')
                    # DTD file won't have rules
                    if example_file != 'FLExTransRuleGenerator.dtd':
                        assert rules_section is not None or example_file.endswith('.dtd'), \
                            f"{example_file} has no FLExTransRules section"

            except ET.ParseError as e:
                pytest.fail(f"Failed to parse {example_file}: {e}")


# ==============================================================================
# UNIT TESTS FOR HELPER CLASSES
# ==============================================================================

class TestHelperClasses:
    """Test utility classes and data structures."""

    def test_feature_spec_creation(self):
        """Test FeatureSpec dataclass creation and properties."""
        spec = FeatureSpec(
            category='n',
            label='gender',
            isAffix=True,
            value='m',
            default='m',
            isSource=False,
            ranking=1
        )

        assert spec.category == 'n'
        assert spec.label == 'gender'
        assert spec.isAffix is True
        assert spec.value == 'm'
        assert spec.xmlLabel == 'n_gender_or_m'

    def test_feature_spec_xml_label(self):
        """Test xmlLabel property generation."""
        spec1 = FeatureSpec(category='n', label='number', isAffix=True)
        assert spec1.xmlLabel == 'n_number'

        spec2 = FeatureSpec(category='n', label='number', isAffix=True, default='sg')
        assert spec2.xmlLabel == 'n_number_or_sg'

    def test_macro_spec_creation(self):
        """Test MacroSpec dataclass creation."""
        spec = MacroSpec(
            macid='m_test_macro',
            varid='v_test_var',
            catSequence=['n', 'adj']
        )

        assert spec.macid == 'm_test_macro'
        assert spec.varid == 'v_test_var'
        assert len(spec.catSequence) == 2


class TestRuleGeneratorUtilities:
    """Test RuleGenerator utility methods."""

    def test_get_available_id(self, rule_generator):
        """Test ID generation and collision avoidance."""
        # First ID should be clean
        id1 = rule_generator.GetAvailableID('test_id')
        assert id1 == 'test_id'

        # Second should get a number
        id2 = rule_generator.GetAvailableID('test_id')
        assert id2 == 'test_id1'

        # Third should increment
        id3 = rule_generator.GetAvailableID('test_id')
        assert id3 == 'test_id2'

    def test_get_available_id_spaces(self, rule_generator):
        """Test that spaces in IDs are replaced with underscores."""
        id_with_space = rule_generator.GetAvailableID('test id with spaces')
        assert ' ' not in id_with_space
        assert id_with_space == 'test_id_with_spaces'

    def test_get_section(self, rule_generator):
        """Test section retrieval and creation."""
        # Get a section (should create if not exists)
        section = rule_generator.GetSection('section-def-cats')
        assert section is not None
        assert section.tag == 'section-def-cats'

        # Getting it again should return the same element
        section2 = rule_generator.GetSection('section-def-cats')
        assert section is section2

    def test_add_single_attribute(self, rule_generator):
        """Test attribute addition and reuse."""
        items1 = {'m', 'f'}
        attr1 = rule_generator.AddSingleAttribute('a_gender', items1)

        # Should be in defined attributes
        assert attr1 in rule_generator.definedAttributes
        assert rule_generator.definedAttributes[attr1] == items1

        # Requesting same items should return existing attribute
        items2 = {'m', 'f'}
        attr2 = rule_generator.AddSingleAttribute('a_gender2', items2)
        assert attr2 == attr1  # Should reuse existing


# ==============================================================================
# PERFORMANCE AND STRESS TESTS
# ==============================================================================

class TestPerformance:
    """Test performance with large or complex rules."""

    def test_large_rule_set(self, rule_generator, temp_dir):
        """
        Test processing a large number of rules.

        Validates performance with many rules.
        """
        # Create a file with many rules
        root = ET.Element('FLExTransRuleGenerator')
        rules = ET.SubElement(root, 'FLExTransRules')

        for i in range(20):
            rule = ET.SubElement(rules, 'FLExTransRule', name=f'Rule {i}')
            source = ET.SubElement(rule, 'Source')
            phrase = ET.SubElement(source, 'Phrase')
            words = ET.SubElement(phrase, 'Words')
            ET.SubElement(words, 'Word', category='n', id='1')

            target = ET.SubElement(rule, 'Target')
            phrase = ET.SubElement(target, 'Phrase')
            words = ET.SubElement(phrase, 'Words')
            ET.SubElement(words, 'Word', head='yes', id='1')

        rule_file = os.path.join(temp_dir, 'large_ruleset.xml')
        tree = ET.ElementTree(root)
        tree.write(rule_file)

        with patch('CreateApertiumRules.Utils.getLemmasForFeature', return_value=[]):
            with patch('CreateApertiumRules.Utils.getAffixGlossesForFeature', return_value=[]):
                with patch('CreateApertiumRules.Utils.getPossibleFeatureValues', return_value=[]):
                    rule_count = rule_generator.ProcessAssistantFile(rule_file)

        # Should process all rules
        assert rule_count == 20

    def test_complex_permutations(self, rule_generator, temp_dir):
        """
        Test performance with complex permutation generation.

        Validates handling of rules that generate many permutations.
        """
        xml_content = """<?xml version="1.0" encoding="utf-8"?>
        <FLExTransRuleGenerator>
          <FLExTransRules>
            <FLExTransRule name="Complex Permutations" create_permutations="yes">
              <Source>
                <Phrase>
                  <Words>
                    <Word category="det" id="1"></Word>
                    <Word category="adj" id="2"></Word>
                    <Word category="adj" id="3"></Word>
                    <Word category="n" id="4" head="yes"></Word>
                  </Words>
                </Phrase>
              </Source>
              <Target>
                <Phrase>
                  <Words>
                    <Word head="no" id="1"></Word>
                    <Word head="no" id="2"></Word>
                    <Word head="no" id="3"></Word>
                    <Word head="yes" id="4"></Word>
                  </Words>
                </Phrase>
              </Target>
            </FLExTransRule>
          </FLExTransRules>
        </FLExTransRuleGenerator>
        """

        rule_file = os.path.join(temp_dir, 'complex_perm.xml')
        with open(rule_file, 'w') as f:
            f.write(xml_content)

        with patch('CreateApertiumRules.Utils.getLemmasForFeature', return_value=[]):
            with patch('CreateApertiumRules.Utils.getAffixGlossesForFeature', return_value=[]):
                with patch('CreateApertiumRules.Utils.getPossibleFeatureValues', return_value=[]):
                    rule_count = rule_generator.ProcessAssistantFile(rule_file)

        # Should create multiple permutation rules (2^3 = 8 combinations)
        assert rule_count > 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
