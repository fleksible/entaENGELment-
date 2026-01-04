#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "ConsentTypes.h"
#include "SynthosiaGeneratorSubsystem.generated.h"

/**
 * Receipt for a manifest generation operation.
 * Evidence trail for audit compliance.
 */
USTRUCT(BlueprintType)
struct FManifestReceipt
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	FString ReceiptID;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	FString OperationType; // "SPAWN_ACTOR", "SPAWN_NIAGARA", "SPAWN_SOUND"

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	FString ConsentTicketID;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	FDateTime Timestamp;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	bool bSuccess = false;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	FString FailureReason;
};

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnManifestGenerated, const FManifestReceipt&, Receipt);

/**
 * Synthosia Generator Subsystem.
 * The "Manifest-Zoll" - enforcement point for latent->manifest transition.
 *
 * NOTHING spawns without:
 * 1. Valid Consent Ticket
 * 2. KillSwitch not active
 * 3. Receipt generation
 */
UCLASS()
class SYNTHOSIACORE_API USynthosiaGeneratorSubsystem : public UGameInstanceSubsystem
{
	GENERATED_BODY()

public:
	// === ENFORCEMENT GATES ===

	/**
	 * Check if generation is allowed (Consent + KillSwitch).
	 * @param Ticket The consent ticket for this operation
	 * @param OutReason Reason if denied
	 * @return true if generation is allowed
	 */
	UFUNCTION(BlueprintCallable, Category = "Synthosia|Generator")
	bool CanGenerate(const FConsentTicket& Ticket, FString& OutReason) const;

	/**
	 * Attempt to spawn with full enforcement.
	 * Creates receipt, validates consent, checks killswitch.
	 * @param Ticket The consent ticket
	 * @param OperationType Type of operation
	 * @param OutReceipt The generated receipt
	 * @return true if spawn was allowed
	 */
	UFUNCTION(BlueprintCallable, Category = "Synthosia|Generator")
	bool TryGenerate(
		const FConsentTicket& Ticket,
		const FString& OperationType,
		FManifestReceipt& OutReceipt);

	// === EVENTS ===

	UPROPERTY(BlueprintAssignable, Category = "Synthosia|Generator")
	FOnManifestGenerated OnManifestGenerated;

	// === AUDIT ===

	UFUNCTION(BlueprintPure, Category = "Synthosia|Generator")
	const TArray<FManifestReceipt>& GetReceiptLog() const { return ReceiptLog; }

	UFUNCTION(BlueprintPure, Category = "Synthosia|Generator")
	int32 GetTotalGenerations() const { return TotalGenerations; }

	UFUNCTION(BlueprintPure, Category = "Synthosia|Generator")
	int32 GetBlockedGenerations() const { return BlockedGenerations; }

private:
	TArray<FManifestReceipt> ReceiptLog;
	int32 TotalGenerations = 0;
	int32 BlockedGenerations = 0;

	FString GenerateReceiptID() const;
};
