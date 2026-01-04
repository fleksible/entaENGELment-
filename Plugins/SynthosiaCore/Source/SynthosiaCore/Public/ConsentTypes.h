#pragma once

#include "CoreMinimal.h"
#include "ConsentTypes.generated.h"

/**
 * G0: Der Consent-Zustand.
 * In Synthosia ist "Keine Antwort" immer "Nein".
 */
UENUM(BlueprintType)
enum class EConsentState : uint8
{
	UNKNOWN     UMETA(DisplayName = "Unknown (Blocked)"),
	REQUESTED   UMETA(DisplayName = "Requested (Wait)"),
	GRANTED     UMETA(DisplayName = "Granted (Active)"),
	DENIED      UMETA(DisplayName = "Denied (Blocked)"),
	REVOKED     UMETA(DisplayName = "Revoked (Immediate Stop)")
};

/**
 * Ein "Ticket" für eine bio-elektrische Operation.
 * Ohne dieses Ticket darf Niagara nicht starten.
 */
USTRUCT(BlueprintType)
struct FConsentTicket
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	FString TicketID;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	EConsentState State = EConsentState::UNKNOWN;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	FDateTime Timestamp;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	FString Context; // Wofür? (z.B. "BioFeedback_Haptics")
};
