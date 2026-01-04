#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "KillSwitch.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnKillSwitchTriggered);

/**
 * G5: Kill-Switch Subsystem.
 * Die absolute Autorität über die Runtime.
 * Eine Hardware-nahe Sicherung in Software.
 */
UCLASS()
class SYNTHOSIACORE_API UKillSwitchSubsystem : public UGameInstanceSubsystem
{
	GENERATED_BODY()

public:
	// Status abfragen (Poll)
	UFUNCTION(BlueprintPure, Category = "Synthosia|Safety")
	bool IsKillSwitchActive() const { return bIsActive; }

	// Not-Aus auslösen (Irreversibel für die Session)
	UFUNCTION(BlueprintCallable, Category = "Synthosia|Safety")
	void TriggerKillSwitch(FString Reason);

	// Event-Hook für alle anderen Systeme
	UPROPERTY(BlueprintAssignable, Category = "Synthosia|Safety")
	FOnKillSwitchTriggered OnKillSwitchTriggered;

private:
	bool bIsActive = false;
	FString TriggerReason;
};
