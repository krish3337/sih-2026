export const analyzeSpecification = async (payload) => {
  const { type, content, language } = payload;

  if (!content) {
    throw new Error("No content provided");
  }

  try {
    const response = await fetch('http://localhost:8000/v1/recommend', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: content,
        language_hint: language || 'en'
      }),
    });

    if (!response.ok) {
      throw new Error(`API returned ${response.status}`);
    }

    const data = await response.json();
    
    // Map backend data to what the extension UI expects
    const standards = (data.recommendations || []).map(std => {
      const relevanceScore = Math.round((std.similarity_score || 0) * 100);
      let applicability = 'LOW';
      if (relevanceScore >= 90) applicability = 'HIGH';
      else if (relevanceScore >= 75) applicability = 'RELATED';
      
      return {
        code: std.standard_id,
        title: std.title,
        applicability,
        status: std.certification?.mandatory ? "Mandatory" : "Voluntary",
        explanation: data.explanation || "No explanation provided."
      };
    });

    return { standards };
  } catch (error) {
    console.error("API Error:", error);
    throw new Error("Failed to analyze text. Ensure the backend server is running.");
  }
};
