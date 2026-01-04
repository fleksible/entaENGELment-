#pragma once

#include "CoreMinimal.h"
#include "BifrostCaduceus.generated.h"

/**
 * MOD_10: Hopf Fibration / Bifrost Geometry Library.
 * Generates deterministic fiber bundles for Niagara/visualization.
 *
 * Hardened against:
 * - FiberCount=0 (division by zero)
 * - HSV overflow (uint8 clamping)
 * - Memory pre-allocation (deterministic)
 */
USTRUCT(BlueprintType)
struct FBifrostFiberPoint
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	FVector Position = FVector::ZeroVector;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	FLinearColor Color = FLinearColor::White;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	float FiberAlpha = 0.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	float StepAlpha = 0.0f;
};

/**
 * Bifrost Caduceus Generator.
 * Creates intertwined helical fibers (S3 -> S2 projection).
 */
UCLASS(BlueprintType)
class SYNTHOSIACORE_API UBifrostCaduceus : public UObject
{
	GENERATED_BODY()

public:
	/**
	 * Generate Hopf fibration points.
	 * @param FiberCount Number of fibers (must be > 0)
	 * @param BaseRadius Base radius of the structure
	 * @param TwistRate Helical twist rate
	 * @param OutPoints Output array of fiber points
	 */
	UFUNCTION(BlueprintCallable, Category = "Synthosia|Geometry")
	static void GenerateHopfFibration(
		int32 FiberCount,
		float BaseRadius,
		float TwistRate,
		TArray<FBifrostFiberPoint>& OutPoints)
	{
		OutPoints.Reset();

		// HARDENING: Prevent division by zero
		if (FiberCount <= 0)
		{
			UE_LOG(LogTemp, Warning, TEXT("BifrostCaduceus: FiberCount must be > 0"));
			return;
		}

		// HARDENING: Use int32 for loop clarity
		const int32 StepsPerFiber = 50;

		// HARDENING: Pre-allocate for deterministic memory
		OutPoints.Reserve(FiberCount * StepsPerFiber);

		for (int32 i = 0; i < FiberCount; ++i)
		{
			const float FiberAlpha = static_cast<float>(i) / static_cast<float>(FiberCount);
			const float FiberAngle = FiberAlpha * 2.0f * PI;

			// HARDENING: Clamp and cast to uint8 for MakeFromHSV8
			const uint8 Hue = static_cast<uint8>(FMath::Clamp(
				FMath::RoundToInt(FiberAlpha * 255.0f), 0, 255));
			const FLinearColor FiberColor = FLinearColor::MakeFromHSV8(Hue, 255, 255);

			for (int32 j = 0; j < StepsPerFiber; ++j)
			{
				const float StepAlpha = static_cast<float>(j) / static_cast<float>(StepsPerFiber);
				const float T = StepAlpha * 2.0f * PI;

				// Hopf fibration parametrization (S3 -> S2)
				const float R = BaseRadius * (1.0f + 0.3f * FMath::Sin(T * TwistRate));
				const float X = R * FMath::Cos(FiberAngle + T * TwistRate);
				const float Y = R * FMath::Sin(FiberAngle + T * TwistRate);
				const float Z = BaseRadius * 0.5f * FMath::Sin(T * 2.0f);

				FBifrostFiberPoint Point;
				Point.Position = FVector(X, Y, Z);
				Point.Color = FiberColor;
				Point.FiberAlpha = FiberAlpha;
				Point.StepAlpha = StepAlpha;

				OutPoints.Add(Point);
			}
		}
	}

	/**
	 * Generate Caduceus (twin helix) geometry.
	 * @param Turns Number of helical turns
	 * @param BaseRadius Base radius
	 * @param HelixSeparation Separation between twin helices
	 * @param OutPoints Output array of fiber points
	 */
	UFUNCTION(BlueprintCallable, Category = "Synthosia|Geometry")
	static void GenerateCaduceus(
		int32 Turns,
		float BaseRadius,
		float HelixSeparation,
		TArray<FBifrostFiberPoint>& OutPoints)
	{
		OutPoints.Reset();

		if (Turns <= 0)
		{
			UE_LOG(LogTemp, Warning, TEXT("BifrostCaduceus: Turns must be > 0"));
			return;
		}

		const int32 PointsPerTurn = 36;
		const int32 TotalPoints = Turns * PointsPerTurn;

		// Pre-allocate for both helices
		OutPoints.Reserve(TotalPoints * 2);

		for (int32 Helix = 0; Helix < 2; ++Helix)
		{
			const float PhaseOffset = Helix * PI;
			const uint8 Hue = Helix == 0 ? 0 : 128; // Red vs Cyan
			const FLinearColor HelixColor = FLinearColor::MakeFromHSV8(Hue, 255, 255);

			for (int32 i = 0; i < TotalPoints; ++i)
			{
				const float Alpha = static_cast<float>(i) / static_cast<float>(TotalPoints);
				const float Angle = Alpha * Turns * 2.0f * PI + PhaseOffset;
				const float Height = Alpha * BaseRadius * 4.0f;

				const float X = BaseRadius * FMath::Cos(Angle);
				const float Y = BaseRadius * FMath::Sin(Angle);
				const float Z = Height;

				FBifrostFiberPoint Point;
				Point.Position = FVector(X, Y, Z);
				Point.Color = HelixColor;
				Point.FiberAlpha = static_cast<float>(Helix);
				Point.StepAlpha = Alpha;

				OutPoints.Add(Point);
			}
		}
	}
};
