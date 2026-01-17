#pragma once

#include "CoreMinimal.h"
#include "RCC8.generated.h"

/**
 * RCC8: Region Connection Calculus with 8 base relations.
 * Topological relations between spatial regions.
 * Used for MOD_11 spatial reasoning and consent-boundary checks.
 */
UENUM(BlueprintType)
enum class ERCC8 : uint8
{
	DC       UMETA(DisplayName = "Disconnected"),
	EC       UMETA(DisplayName = "Externally Connected"),
	PO       UMETA(DisplayName = "Partial Overlap"),
	EQ       UMETA(DisplayName = "Equal"),
	TPP      UMETA(DisplayName = "Tangential Proper Part"),
	NTPP     UMETA(DisplayName = "Non-Tangential Proper Part"),
	TPPi     UMETA(DisplayName = "Tangential Proper Part Inverse"),
	NTPPi    UMETA(DisplayName = "Non-Tangential Proper Part Inverse")
};

/**
 * Helper to check if relation implies containment.
 */
FORCEINLINE bool RCC8_ImpliesContainment(ERCC8 Relation)
{
	return Relation == ERCC8::TPP ||
	       Relation == ERCC8::NTPP ||
	       Relation == ERCC8::EQ;
}

/**
 * Helper to check if relation implies boundary contact.
 */
FORCEINLINE bool RCC8_ImpliesBoundaryContact(ERCC8 Relation)
{
	return Relation == ERCC8::EC ||
	       Relation == ERCC8::TPP ||
	       Relation == ERCC8::TPPi;
}
