/**
 * TYC THAILAND — ORGANIZATION TAILWIND CONFIG (v3-compatible)
 * ---------------------------------------------------------------------
 * ไฟล์นี้เป็น theme กลางขององค์กร แยกต่างหาก ไม่ผูกกับโปรเจกต์ใดโปรเจกต์หนึ่ง
 * ใช้กับโปรเจกต์ Tailwind CSS v3 ใดก็ได้ — copy ไปวางที่ root แล้วปรับ `content`
 * ให้ตรงกับ path ของโปรเจกต์นั้นๆ
 *
 * หมายเหตุ: ถ้าโปรเจกต์เป็น Tailwind v4 (CSS-first, ไม่มีไฟล์ config) ให้ใช้
 * tyc-design-tokens.css แทน — ไฟล์นั้นคือ token ชุดเดียวกัน เขียนในรูปแบบที่
 * Tailwind v4 ใช้งานได้ตรง (@theme inline + OKLCH)
 *
 * สีอ้างอิงจาก Brand Guideline จริง — PANTONE 2173 C / 213 C / 5435 C / 6 C
 * ล็อกตรงกับ theme-ui-guideline.html และ tyc-design-tokens.json ทุกค่า
 * ---------------------------------------------------------------------
 */

/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: "class",
  content: [
    "./src/**/*.{js,ts,jsx,tsx,mdx,html}",
    "./app/**/*.{js,ts,jsx,tsx,mdx,html}",
    "./pages/**/*.{js,ts,jsx,tsx,mdx,html}",
    "./components/**/*.{js,ts,jsx,tsx,mdx,html}",
  ],
  theme: {
    extend: {
      // ---- Colors ----------------------------------------------------
      colors: {
        primary: {
          DEFAULT: "#0172E5", // PANTONE 2173 C — สีหลัก ~75% ของสัดส่วนสี
          hover: "#015BB7",
          soft: "#E7F1FD",
          foreground: "#FFFFFF",
        },
        secondary: {
          DEFAULT: "#A5BBCB", // PANTONE 5435 C — Grey-Blue
          foreground: "#1F2430",
        },
        accent: {
          DEFAULT: "#E81F76", // PANTONE 213 C — decorative accent เท่านั้น ~25%
          foreground: "#FFFFFF",
        },
        dark: {
          DEFAULT: "#22242D", // PANTONE 6 C — Near-black, พื้น Sidebar
          soft: "#2E313C",
          border: "#383B47",
        },
        background: "#F4F5F7",
        surface: "#FFFFFF",
        "text-main": "#1F2430",
        "text-muted": "#6B7280",
        border: "#E3E6EB",

        // ---- Dark surface (product dark theme, ไม่ใช่ sidebar) --------
        "dark-surface": {
          page: "#16171D",
          panel: "#22242D",
          input: "#33353E",
          border: "#454852",
          muted: "#A5BBCB",
          link: "#73B1F1",
        },

        // ---- Status (semantic — แยกจากสีแบรนด์) -----------------------
        success: { DEFAULT: "#16A34A", bg: "#DCFCE7", text: "#166534" },
        warning: { DEFAULT: "#D97706", bg: "#FEF3C7", text: "#92400E" },
        danger: { DEFAULT: "#DC2626", bg: "#FEE2E2", text: "#991B1B", ondark: "#FF9187" },
      },

      // ---- Border radius — --radius-md: 6px คือค่ามาตรฐานหลักของระบบ
      // ข้อยกเว้น: ปุ่ม (<button>, .btn) ทุกแบบใช้ rounded-pill เสมอ ตามระบบจริง
      // (WMS/Work order) — ยกเว้นปุ่มไอคอนเดี่ยวที่ยังใช้ rounded-md ------
      borderRadius: {
        sm: "4px",
        md: "6px",
        lg: "10px",
        pill: "999px",
      },

      // ---- Font — Sarabun คือฟอนต์จริงของระบบ (rcs-rmr-pm), Prompt สำรอง
      fontFamily: {
        sans: ["Sarabun", "Prompt", "Inter", "-apple-system", "Segoe UI", "sans-serif"],
      },

      // ---- Spacing scale (4pt grid) — เสริมจาก default scale ของ Tailwind
      spacing: {
        4.5: "18px",
      },

      // ---- Shadow / Elevation -----------------------------------------
      boxShadow: {
        sm: "0 1px 2px rgba(17, 24, 39, .06)",
        md: "0 4px 14px rgba(17, 24, 39, .08)",
        lg: "0 12px 32px rgba(17, 24, 39, .12)",
        "btn-primary": "0 6px 14px -6px rgba(1, 114, 229, .55)",
      },

      // ---- Layout tokens ที่ใช้ซ้ำบ่อยในระบบ Sidebar + Header ---------
      width: {
        sidebar: "260px",
      },
      height: {
        header: "64px",
      },
    },
  },
  plugins: [],
};
