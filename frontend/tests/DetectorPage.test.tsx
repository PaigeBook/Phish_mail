import { render, screen } from "@testing-library/react";
import { vi } from "vitest";

import DetectorPage from "../features/detector/DetectorPage";

vi.mock("../shared/hooks/useAnalyzeEmail", () => ({
  useAnalyzeEmail: () => ({
    mutateAsync: vi.fn(),
    isPending: false,
    isError: false,
    data: null
  })
}));

test("renders detector page", () => {
  render(<DetectorPage />);
  expect(screen.getByText(/Phishing Email Detector/i)).toBeInTheDocument();
  expect(screen.getByRole("button", { name: /Analyze Email/i })).toBeVisible();
});
