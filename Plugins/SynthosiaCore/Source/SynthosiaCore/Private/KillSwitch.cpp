#include "KillSwitch.h"

void UKillSwitchSubsystem::TriggerKillSwitch(FString Reason)
{
	// Wenn schon tot, dann ignorieren (Idempotenz)
	if (bIsActive) return;

	bIsActive = true;
	TriggerReason = Reason;

	// Hard Log in die Console (Beweissicherung)
	UE_LOG(LogTemp, Error, TEXT("!!! KILL SWITCH TRIGGERED !!! Reason: %s"), *Reason);

	// Broadcast: Alle Systeme müssen sofort stoppen
	if (OnKillSwitchTriggered.IsBound())
	{
		OnKillSwitchTriggered.Broadcast();
	}
}
