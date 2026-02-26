import "./globals.css";

import { IBM_Plex_Sans, Space_Grotesk } from "next/font/google";
import type { ReactNode } from "react";

import Providers from "@/shared/components/Providers";

const headingFont = Space_Grotesk({ subsets: ["latin"], weight: ["400", "600"] });
const bodyFont = IBM_Plex_Sans({ subsets: ["latin"], weight: ["300", "400", "600"] });

export const metadata = {
  title: "🐠 Safe Harbor - Phishing Email Detector",
  description: "Keep your inbox safe from phishing nets with AI-powered protection"
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body className={`${bodyFont.className} bg-bone`}>
        <Providers>
          <div className={headingFont.className}>{children}</div>
        </Providers>
      </body>
    </html>
  );
}
