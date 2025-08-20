// src/hooks/useTfModel.ts
import * as tf from "@tensorflow/tfjs";
import "@tensorflow/tfjs-react-native";
import { useEffect, useState } from "react";

export const useTfModel = () => {
  const [model, setModel] = useState<tf.GraphModel | null>(null);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    const load = async () => {
      await tf.ready();
      console.log("TFJS ready ✅");

      const modelJson = require("../../assets/model/model.json");
      const loadedModel = await tf.loadGraphModel(modelJson);
      setModel(loadedModel);
      setReady(true);
    };

    load();
  }, []);

  return { model, ready };
};
