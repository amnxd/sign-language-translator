// src/screens/HomeScreen.tsx
import * as tf from "@tensorflow/tfjs";
import { cameraWithTensors } from "@tensorflow/tfjs-react-native";
import { Camera } from "expo-camera";
import React, { useEffect, useRef, useState } from "react";
import { Text, View } from "react-native";
import { useTfModel } from "../../hooks/useTfModel";
import { preprocessFrame } from "../../hooks/utils";
import PredictionResult from "./components/PredictionResult";

const TensorCamera = cameraWithTensors(Camera);

export default function HomeScreen() {
  const { model, ready } = useTfModel();
  const [prediction, setPrediction] = useState<number[] | null>(null);
  const [hasPermission, setHasPermission] = useState<boolean | null>(null);

  const textureDims = { height: 192, width: 192 }; // Camera texture size
  const cameraRef = useRef<any>(null);

  useEffect(() => {
    (async () => {
      const { status } = await Camera.requestCameraPermissionsAsync();
      setHasPermission(status === "granted");
    })();
  }, []);

  const handleCameraStream = (images: any) => {
    const loop = async () => {
      if (!model) return;

      const nextImageTensor = images.next().value as tf.Tensor4D;
      const inputTensor = preprocessFrame(nextImageTensor, 224); // preprocess to 224x224
      nextImageTensor.dispose();

      const output = model.predict(inputTensor) as tf.Tensor;
      const values = Array.from(await output.data());
      setPrediction(values);

      inputTensor.dispose();
      requestAnimationFrame(loop);
    };
    loop();
  };

  if (hasPermission === null) return <Text>Requesting camera permission...</Text>;
  if (hasPermission === false) return <Text>No access to camera</Text>;

  return (
    <View style={{ flex: 1, backgroundColor: "black" }}>
      {ready && model ? (
        <TensorCamera
          ref={cameraRef}
          style={{ flex: 1 }}
          type={Camera.Constants.Type.front}
          cameraTextureHeight={textureDims.height}
          cameraTextureWidth={textureDims.width}
          resizeHeight={textureDims.height}
          resizeWidth={textureDims.width}
          resizeDepth={3}
          onReady={handleCameraStream}
          autorender={true}
        />
      ) : (
        <Text style={{ color: "white" }}>Loading Model...</Text>
      )}
      <PredictionResult prediction={prediction} />
    </View>
  );
}
