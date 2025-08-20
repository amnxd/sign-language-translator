// src/components/PredictionResult.tsx
import React from "react";
import { Text, View } from "react-native";

type Props = {
  prediction: number[] | null;
};

export default function PredictionResult({ prediction }: Props) {
  if (!prediction) return <Text>No prediction yet...</Text>;

  return (
    <View style={{ position: "absolute", bottom: 20, left: 20 }}>
      <Text style={{ fontSize: 18, fontWeight: "bold", color: "white" }}>
        Prediction: {prediction.map(v => v.toFixed(2)).join(", ")}
      </Text>
    </View>
  );
}
