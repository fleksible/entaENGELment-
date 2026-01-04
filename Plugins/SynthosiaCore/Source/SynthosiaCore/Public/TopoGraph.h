#pragma once

#include "CoreMinimal.h"
#include "RCC8.h"
#include "TopoGraph.generated.h"

/**
 * A node in the topological graph.
 * Represents a region/zone with optional metadata.
 */
USTRUCT(BlueprintType)
struct FTopoNode
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	FString NodeID;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	FVector Centroid = FVector::ZeroVector;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	float Radius = 100.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	TMap<FString, FString> Metadata;

	bool IsValid() const { return !NodeID.IsEmpty() && Radius > 0.0f; }
};

/**
 * An edge in the topological graph.
 * Encodes RCC8 relation between two nodes.
 */
USTRUCT(BlueprintType)
struct FTopoEdge
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	FString SourceID;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	FString TargetID;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	ERCC8 Relation = ERCC8::DC;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	float Weight = 1.0f;

	bool IsValid() const { return !SourceID.IsEmpty() && !TargetID.IsEmpty(); }
};

/**
 * A complete topological graph structure.
 * Used for spatial reasoning and consent-zone mapping.
 */
USTRUCT(BlueprintType)
struct FTopoGraph
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	FString GraphID;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	TArray<FTopoNode> Nodes;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	TArray<FTopoEdge> Edges;

	// Find node by ID
	const FTopoNode* FindNode(const FString& NodeID) const
	{
		for (const FTopoNode& Node : Nodes)
		{
			if (Node.NodeID == NodeID) return &Node;
		}
		return nullptr;
	}

	// Find all edges from a node
	TArray<FTopoEdge> GetOutgoingEdges(const FString& NodeID) const
	{
		TArray<FTopoEdge> Result;
		for (const FTopoEdge& Edge : Edges)
		{
			if (Edge.SourceID == NodeID) Result.Add(Edge);
		}
		return Result;
	}

	// Check if two nodes are connected
	bool AreConnected(const FString& A, const FString& B) const
	{
		for (const FTopoEdge& Edge : Edges)
		{
			if ((Edge.SourceID == A && Edge.TargetID == B) ||
			    (Edge.SourceID == B && Edge.TargetID == A))
			{
				return Edge.Relation != ERCC8::DC;
			}
		}
		return false;
	}
};
