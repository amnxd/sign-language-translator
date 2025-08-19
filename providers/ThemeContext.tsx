import { useColorScheme } from '@/hooks/useColorScheme';
import React, { createContext, useCallback, useContext, useMemo, useState } from 'react';
import { ColorSchemeName } from 'react-native';

type ThemeContextValue = {
  colorScheme: NonNullable<ColorSchemeName>;
  toggleColorScheme: () => void;
};

export const ThemeContext = createContext<ThemeContextValue | undefined>(undefined);

export function AppThemeProvider({ children }: { children: React.ReactNode }) {
  const initialScheme = (useColorScheme() ?? 'dark') as NonNullable<ColorSchemeName>;
  const [colorScheme, setColorScheme] = useState<NonNullable<ColorSchemeName>>(initialScheme);

  const toggleColorScheme = useCallback(() => {
    setColorScheme(prev => (prev === 'dark' ? 'light' : 'dark'));
  }, []);

  const value = useMemo(() => ({ colorScheme, toggleColorScheme }), [colorScheme, toggleColorScheme]);

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}

export function useTheme() {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error('useTheme must be used within AppThemeProvider');
  return ctx;
}


