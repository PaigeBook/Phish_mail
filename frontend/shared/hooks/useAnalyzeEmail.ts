import { useMutation } from "@tanstack/react-query";

import { analyzeEmail } from "../lib/api";

export function useAnalyzeEmail() {
  return useMutation({
    mutationFn: analyzeEmail
  });
}
