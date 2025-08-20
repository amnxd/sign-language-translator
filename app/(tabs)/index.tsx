import { Platform, Pressable, SafeAreaView, StatusBar, StyleSheet, View } from 'react-native';

import { useTheme } from '@/providers/ThemeContext';
import { ThemedText } from '@/src/components/ThemedText';
import { ThemedView } from '@/src/components/ThemedView';
// src/App.tsx
import React from "react";






export default function HomeScreen() {
  const { colorScheme } = useTheme();
  const borderColor = colorScheme === 'dark' ? 'rgba(255,255,255,0.35)' : '#E2E2E2';
  return (
    <><SafeAreaView style={{ flex: 1 }}>
      <StatusBar barStyle="dark-content" />
      <HomeScreen />
    </SafeAreaView><ThemedView
      style={[
        styles.screenContainer,
        Platform.OS === 'web' ? styles.screenContainerWeb : styles.mobileContainer,
      ]}
    >
        {Platform.OS === 'web' ? (
          <>
            <View style={styles.webRow}>
              <View style={styles.webLeft}>
                <ThemedText style={styles.sectionLabel}>Capture</ThemedText>
                <ThemedView style={[styles.card, styles.cameraCard, styles.cameraCardWeb, { borderWidth: 1, borderColor }]} />
              </View>
              <View style={styles.webRight}>
                <Pressable
                  onPress={() => { } }
                  style={({ hovered, pressed }) => [
                    styles.startButton,
                    styles.startButtonWeb,
                    (hovered || pressed) && styles.startButtonHover,
                  ]}
                >
                  <ThemedText style={styles.startButtonText}>Start/Stop</ThemedText>
                </Pressable>
              </View>
            </View>
            <ThemedView style={[styles.card, styles.outputPanel, styles.outputPanelWeb, { borderWidth: 1, borderColor }]}>
              <ThemedText style={styles.outputText}>output</ThemedText>
            </ThemedView>
          </>
        ) : (
          <>
            <View style={styles.contentArea}>
              <ThemedView style={[styles.card, styles.cameraCard, styles.cameraCardMobile, { borderWidth: 1, borderColor }]} />
              <ThemedText style={[styles.sectionLabel, styles.mobileSectionLabel]}>Capture</ThemedText>
            </View>
            <Pressable
              onPress={() => { } }
              style={({ hovered, pressed }) => [
                styles.startButton,
                styles.startButtonMobile,
                (hovered || pressed) && styles.startButtonHover,
              ]}
            >
              <ThemedText style={styles.startButtonText}>Start/Stop</ThemedText>
            </Pressable>
            <ThemedView style={[styles.card, styles.outputPanel, { borderWidth: 1, borderColor }]}>
              <ThemedText style={styles.outputText}>output</ThemedText>
            </ThemedView>
          </>
        )}
      </ThemedView></>
    
  );
}

const styles = StyleSheet.create({
  screenContainer: {
    flex: 1,
    paddingHorizontal: 20,
    paddingTop: 40,
    paddingBottom: 16,
    gap: 16,
  },
  contentArea: {
    flex: 1,
    gap: 16,
  },
  screenContainerWeb: {
    justifyContent: 'space-between',
  },
  webRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 24,
    flexGrow: 0,
  },
  webLeft: {
    flex: 1,
  },
  webRight: {
    justifyContent: 'center',
    width: 260,
    paddingHorizontal: 24,
    alignItems: 'stretch',
  },
  card: {
    borderRadius: 18,
    borderWidth: 0,
    padding: 16,
    justifyContent: 'center',
  },
  cameraCard: {
    aspectRatio: 4 / 3,
  },
  cameraCardWeb: {
    aspectRatio: 16 / 9,
    width: '50%',
    alignSelf: 'center',
  },
  cameraCardMobile: {
    marginTop: 40,
    width: '100%',
    maxWidth: 520,
    alignSelf: 'center',
  },
  mobileContainer: {
    paddingHorizontal: 12,
  },
  sectionLabel: {
    alignSelf: 'flex-start',
    marginBottom: 8,
    fontSize: 16,
    fontWeight: '600',
  },
  mobileSectionLabel: {
    alignSelf: 'center',
    marginTop: 8,
  },
  startButton: {
    height: 44,
    borderRadius: 12,
    backgroundColor: '#1e7a34',
    alignItems: 'center',
    justifyContent: 'center',
  },
  startButtonWeb: {
    width: '100%',
    height: 56,
    alignSelf: 'auto',
  },
  startButtonMobile: {
    width: '100%',
  },
  startButtonHover: {
    backgroundColor: '#1a6a2d',
  },
  startButtonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '600',
  },
  outputPanel: {
    height: 110,
    backgroundColor: 'transparent',
  },
  outputPanelWeb: {
    alignSelf: 'stretch',
  },
  outputText: {
    textAlign: 'center',
  },
});
