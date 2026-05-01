// src/services/predictionService.js

const BASE_URL = "http://127.0.0.1:8000/api/prediction";

// 🔹 Get Actual vs Predicted (Jan–Apr + KPIs)
export const getActualVsPredicted = async () => {
  try {
    const res = await fetch(`${BASE_URL}/actual-vs-predicted`);

    if (!res.ok) {
      throw new Error("Failed to fetch actual vs predicted data");
    }

    return await res.json();
  } catch (error) {
    console.error("API Error:", error);
    return null;
  }
};

// 🔹 Get Future Forecast (May–Oct)
export const getFutureForecast = async () => {
  try {
    const res = await fetch(`${BASE_URL}/future`);

    if (!res.ok) {
      throw new Error("Failed to fetch future forecast");
    }

    return await res.json();
  } catch (error) {
    console.error("API Error:", error);
    return [];
  }
};