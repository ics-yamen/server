from utils.graphene.enums import (
    convert_enum_to_graphene_enum,
    get_enum_name_from_django_field,
)

from .models import (
    AssessmentRegistry,
    MethodologyAttribute,
    AdditionalDocument,
    Summary,
    SummaryIssue,
    SummaryFocus,
    ScoreRating,
    ScoreAnalyticalDensity,
    Question,
    SummaryFocusSubSectorIssue,
)

AssessmentRegistryCrisisTypeEnum = convert_enum_to_graphene_enum(
    AssessmentRegistry.CrisisType, name='AssessmentRegistryCrisisTypeEnum'
)
AssessmentRegistryPreparednessTypeEnum = convert_enum_to_graphene_enum(
    AssessmentRegistry.PreparednessType, name='AssessmentRegistryPreparednessTypeEnum'
)
AssessmentRegistryExternalSupportTypeEnum = convert_enum_to_graphene_enum(
    AssessmentRegistry.ExternalSupportType, name='AssessmentRegistryExternalTypeEnum'
)
AssessmentRegistryCoordinationTypeEnum = convert_enum_to_graphene_enum(
    AssessmentRegistry.CoordinationType, name='AssessmentRegistryCoordinationTypeEnum'
)
AssessmentRegistryDetailTypeEnum = convert_enum_to_graphene_enum(
    AssessmentRegistry.Type, name='AssessmentRegistryDetailTypeEnum'
)
AssessmentRegistryFamilyTypeEnum = convert_enum_to_graphene_enum(
    AssessmentRegistry.FamilyType, name='AssessmentRegistryFamilyTypeEnum'
)
AssessmentRegistryFrequencyTypeEnum = convert_enum_to_graphene_enum(
    AssessmentRegistry.FrequencyType, name='AssessmentRegistryFrequencyTypeEnum'
)
AssessmentRegistryConfidentialityTypeEnum = convert_enum_to_graphene_enum(
    AssessmentRegistry.ConfidentialityType, name='AssessmentRegistryConfidentialityTypeEnum'
)
AssessmentRegistryLanguageTypeEnum = convert_enum_to_graphene_enum(
    AssessmentRegistry.Language, name='AssessmentRegistryLanguageTypeEnum'
)
AssessmentRegistryFocusTypeEnum = convert_enum_to_graphene_enum(
    AssessmentRegistry.FocusType, name='AssessmentRegistryFocusTypeEnum'
)
AssessmentRegistrySectorTypeEnum = convert_enum_to_graphene_enum(
    AssessmentRegistry.SectorType, name='AssessmentRegistrySectorTypeEnum'
)
AssessmentRegistryProtectionInfoTypeEnum = convert_enum_to_graphene_enum(
    AssessmentRegistry.ProtectionInfoType, name='AssessmentRegistryProtectionInfoTypeEnum'
)
AssessmentRegistryAffectedGroupTypeEnum = convert_enum_to_graphene_enum(
    AssessmentRegistry.AffectedGroupType, name='AssessmentRegistryAffectedGroupTypeEnum'
)
AssessmentRegistryDataCollectionTechniqueTypeEnum = convert_enum_to_graphene_enum(
    MethodologyAttribute.CollectionTechniqueType, name='AssessmentRegistryDataCollectionTechniqueTypeEnum'
)
AssessmentRegistrySamplingApproachTypeEnum = convert_enum_to_graphene_enum(
    MethodologyAttribute.SamplingApproachType, name='AssessmentRegistrySamplingApproachTypeEnum'
)
AssessmentRegistryProximityTypeEnum = convert_enum_to_graphene_enum(
    MethodologyAttribute.ProximityType, name='AssessmentRegistryProximityTypeEnum'
)
AssessmentRegistryUnitOfAnalysisTypeEnum = convert_enum_to_graphene_enum(
    MethodologyAttribute.UnitOfAnalysisType, name='AssessmentRegistryUnitOfAnalysisTypeEnum'
)
AssessmentRegistryUnitOfReportingTypeEnum = convert_enum_to_graphene_enum(
    MethodologyAttribute.UnitOfReportingType, name='AssessmentRegistryUnitOfReportingTypeEnum'
)
AssessmentRegistryDocumentTypeEnum = convert_enum_to_graphene_enum(
    AdditionalDocument.DocumentType, name='AssessmentRegistryDocumentTypeEnum'
)
AssessmentRegistryScoreTypeEnum = convert_enum_to_graphene_enum(
    ScoreRating.ScoreType, name='AssessmentRegistryScoreTypeEnum'
)
AssessmentRegistryAnalysisLevelTypeEnum = convert_enum_to_graphene_enum(
    ScoreAnalyticalDensity.AnalysisLevelCovered, name='AssessmentRegistryAnalysisLevelTypeEnum'
)
AssessmentRegistryAnalysisFigureTypeEnum = convert_enum_to_graphene_enum(
    ScoreAnalyticalDensity.FigureProvidedByAssessement, name='AssessmentRegistryAnalysisFigureTypeEnum'
)
AssessmentRegistryRatingTypeEnum = convert_enum_to_graphene_enum(
    ScoreRating.RatingType, name='AssessmentRegistryRatingType'
)
AssessmentRegistryCNAQuestionSectorTypeEnum = convert_enum_to_graphene_enum(
    Question.QuestionSector, name='AssessmentRegistryCNAQuestionSectorTypeEnum'
)
AssessmentRegistryCNAQuestionSubSectorTypeEnum = convert_enum_to_graphene_enum(
    Question.QuestionSubSector, name='AssessmentRegistryCNAQuestionSubSectorTypeEnum'
)
AssessmentRegistrySummarySectorTypeEnum = convert_enum_to_graphene_enum(
    Summary.Sector, name='AssessmentRegistrySummarySectorTypeEnum'
)
AssessmentRegistrySummaryFocusSectorTypeEnum = convert_enum_to_graphene_enum(
    SummaryFocus.Sector, name='AssessmentRegistrySummaryFocusSectorTypeEnum'
)
AssessmentRegistrySummaryFocusSubSectorTypeEnum = convert_enum_to_graphene_enum(
    SummaryIssue.FocusSubSector, name='AssessmentRegistrySummaryFocusSubSectorTypeEnum'
)
AssessmentRegistrySummarySubSectorTypeEnum = convert_enum_to_graphene_enum(
    SummaryIssue.SubSector, name='AssessmentRegistrySummarySubSectorTypeEnum'
)
enum_map = {
    get_enum_name_from_django_field(field): enum
    for field, enum in (
        (AssessmentRegistry.bg_crisis_type, AssessmentRegistryCrisisTypeEnum),
        (AssessmentRegistry.bg_preparedness, AssessmentRegistryPreparednessTypeEnum),
        (AssessmentRegistry.external_support, AssessmentRegistryExternalSupportTypeEnum),
        (AssessmentRegistry.coordinated_joint, AssessmentRegistryCoordinationTypeEnum),
        (AssessmentRegistry.details_type, AssessmentRegistryDetailTypeEnum),
        (AssessmentRegistry.family, AssessmentRegistryFamilyTypeEnum),
        (AssessmentRegistry.frequency, AssessmentRegistryFrequencyTypeEnum),
        (AssessmentRegistry.confidentiality, AssessmentRegistryConfidentialityTypeEnum),
        (AssessmentRegistry.language, AssessmentRegistryLanguageTypeEnum),
        (AssessmentRegistry.focuses, AssessmentRegistryFocusTypeEnum),
        (AssessmentRegistry.sectors, AssessmentRegistrySectorTypeEnum),
        (AssessmentRegistry.protection_info_mgmts, AssessmentRegistryProtectionInfoTypeEnum),
        (AssessmentRegistry.affected_groups, AssessmentRegistryAffectedGroupTypeEnum),
        (MethodologyAttribute.data_collection_technique, AssessmentRegistryDataCollectionTechniqueTypeEnum),
        (MethodologyAttribute.sampling_approach, AssessmentRegistrySamplingApproachTypeEnum),
        (MethodologyAttribute.proximity, AssessmentRegistryProximityTypeEnum),
        (MethodologyAttribute.unit_of_analysis, AssessmentRegistryUnitOfAnalysisTypeEnum),
        (MethodologyAttribute.unit_of_reporting, AssessmentRegistryUnitOfReportingTypeEnum),
        (AdditionalDocument.document_type, AssessmentRegistryDocumentTypeEnum),
        (ScoreRating.score_type, AssessmentRegistryScoreTypeEnum),
        (ScoreRating.rating, AssessmentRegistryRatingTypeEnum),
        (ScoreAnalyticalDensity.sector, AssessmentRegistrySectorTypeEnum),
        (ScoreAnalyticalDensity.analysis_level_covered, AssessmentRegistryAnalysisLevelTypeEnum),
        (ScoreAnalyticalDensity.figure_provided, AssessmentRegistryAnalysisFigureTypeEnum),
        (SummaryFocusSubSectorIssue.focus, AssessmentRegistryFocusTypeEnum),
        (SummaryIssue.sub_sector, AssessmentRegistrySummarySubSectorTypeEnum),
        (SummaryIssue.focus_sub_sector, AssessmentRegistrySummaryFocusSubSectorTypeEnum),
    )
}
