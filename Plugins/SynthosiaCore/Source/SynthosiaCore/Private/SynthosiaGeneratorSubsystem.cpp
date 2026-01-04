#include "SynthosiaGeneratorSubsystem.h"
#include "KillSwitch.h"

bool USynthosiaGeneratorSubsystem::CanGenerate(
	const FConsentTicket& Ticket,
	FString& OutReason) const
{
	// GATE 1: Check KillSwitch
	if (UGameInstance* GI = GetGameInstance())
	{
		if (UKillSwitchSubsystem* KS = GI->GetSubsystem<UKillSwitchSubsystem>())
		{
			if (KS->IsKillSwitchActive())
			{
				OutReason = TEXT("BLOCK_KILLSWITCH_ACTIVE");
				return false;
			}
		}
	}

	// GATE 2: Check Consent State
	switch (Ticket.State)
	{
		case EConsentState::GRANTED:
			// OK - proceed
			break;

		case EConsentState::UNKNOWN:
			OutReason = TEXT("BLOCK_CONSENT_UNKNOWN");
			return false;

		case EConsentState::REQUESTED:
			OutReason = TEXT("BLOCK_CONSENT_PENDING");
			return false;

		case EConsentState::DENIED:
			OutReason = TEXT("BLOCK_CONSENT_DENIED");
			return false;

		case EConsentState::REVOKED:
			OutReason = TEXT("BLOCK_CONSENT_REVOKED");
			return false;

		default:
			OutReason = TEXT("BLOCK_CONSENT_INVALID");
			return false;
	}

	// GATE 3: Validate Ticket
	if (Ticket.TicketID.IsEmpty())
	{
		OutReason = TEXT("BLOCK_TICKET_EMPTY");
		return false;
	}

	OutReason = TEXT("ALLOW");
	return true;
}

bool USynthosiaGeneratorSubsystem::TryGenerate(
	const FConsentTicket& Ticket,
	const FString& OperationType,
	FManifestReceipt& OutReceipt)
{
	TotalGenerations++;

	// Build receipt
	OutReceipt.ReceiptID = GenerateReceiptID();
	OutReceipt.OperationType = OperationType;
	OutReceipt.ConsentTicketID = Ticket.TicketID;
	OutReceipt.Timestamp = FDateTime::UtcNow();

	// Check gates
	FString Reason;
	if (!CanGenerate(Ticket, Reason))
	{
		OutReceipt.bSuccess = false;
		OutReceipt.FailureReason = Reason;
		BlockedGenerations++;

		UE_LOG(LogTemp, Warning,
			TEXT("Synthosia Generator BLOCKED: %s | Ticket: %s | Op: %s"),
			*Reason, *Ticket.TicketID, *OperationType);
	}
	else
	{
		OutReceipt.bSuccess = true;
		OutReceipt.FailureReason = TEXT("");

		UE_LOG(LogTemp, Log,
			TEXT("Synthosia Generator ALLOWED: Ticket: %s | Op: %s"),
			*Ticket.TicketID, *OperationType);
	}

	// Log receipt
	ReceiptLog.Add(OutReceipt);

	// Broadcast
	if (OnManifestGenerated.IsBound())
	{
		OnManifestGenerated.Broadcast(OutReceipt);
	}

	return OutReceipt.bSuccess;
}

FString USynthosiaGeneratorSubsystem::GenerateReceiptID() const
{
	return FString::Printf(TEXT("RCP_%s_%d"),
		*FDateTime::UtcNow().ToString(TEXT("%Y%m%d%H%M%S")),
		TotalGenerations);
}
