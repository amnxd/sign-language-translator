// src/hooks/utils.ts
import * as tf from "@tensorflow/tfjs";

export const preprocessFrame = (tensor: tf.Tensor4D, inputSize = 224) => {
  return tf.tidy(() => {
    // Resize to model input size
    let resized = tf.image.resizeBilinear(tensor, [inputSize, inputSize]);
    // Normalize to [0,1] range
    let normalized = resized.div(255);
    // Add batch dimension
    let batched = normalized.expandDims(0);
    return batched;
  });
};
