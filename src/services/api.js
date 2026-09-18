export const analyzeSpecification = async (payload) => {
  // Simulate network delay
  await new Promise(resolve => setTimeout(resolve, 1500));
  
  const { type, content, language } = payload;

  if (!content) {
    throw new Error("No content provided");
  }

  // Determine mock response based on payload type
  // In a real app, you would send FormData for PDF, or JSON for text
  
  const titleText = type === 'pdf' ? "Standards related to Uploaded PDF Document" : "Standards related to Specification";

  return {
    standards: [
      {
        code: "IS 2062:2011",
        title: "Hot Rolled Medium and High Tensile Structural Steel",
        applicability: "HIGH",
        status: "Applicable",
        explanation: `Applicable to the specified structural steel requirement (Analyzed in ${language}).`
      },
      {
        code: "IS 800:2007",
        title: "General Construction in Steel",
        applicability: "RELATED",
        status: "Related",
        explanation: "Relevant to structural design requirements."
      }
    ]
  };
};
