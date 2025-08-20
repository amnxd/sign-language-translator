import { Pressable, StyleSheet, View } from 'react-native';

import { useTheme } from '@/providers/ThemeContext';
import { ThemedText } from '@/src/components/ThemedText';
import { ThemedView } from '@/src/components/ThemedView';

export default function SettingsScreen() {
  const { colorScheme, toggleColorScheme } = useTheme();
  const borderColor = colorScheme === 'dark' ? 'rgba(255,255,255,0.35)' : '#E2E2E2';
  return (
    <ThemedView style={styles.screenContainer}>
      <View style={styles.headerRow}>
        <Pressable
          accessibilityRole="button"
          accessibilityLabel="Toggle theme"
          onPress={toggleColorScheme}
          style={({ hovered, pressed }) => [
            styles.themeToggle,
            { borderColor },
            (hovered || pressed) && styles.themeToggleHover,
          ]}
        >
          <ThemedText style={styles.themeToggleText}>{colorScheme === 'dark' ? '☀️' : '🌙'}</ThemedText>
        </Pressable>
      </View>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  screenContainer: {
    flex: 1,
    paddingHorizontal: 20,
    paddingTop: 20,
  },
  headerRow: {
    alignItems: 'flex-end',
    marginTop: 60,
  },
  themeToggle: {
    width: 52,
    height: 52,
    borderRadius: 26,
    borderWidth: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  themeToggleHover: {
    backgroundColor: 'rgba(127,127,127,0.15)',
  },
  themeToggleText: {
    fontSize: 20,
  },
});
