import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000";

// =====================================================
// ACTUAL VS PREDICTED
// =====================================================

export const getActualVsPredicted = async () => {

  try {

    const response = await axios.get(
      `${BASE_URL}/api/prediction/actual-vs-predicted`
    );

    return response.data;

  } catch (error) {

    console.error(
      "Actual vs Predicted API Error:",
      error
    );

    return null;
  }
};

// =====================================================
// FUTURE FORECAST
// =====================================================

export const getFutureForecast = async () => {

  try {

    const response = await axios.get(
      `${BASE_URL}/api/prediction/future`
    );

    return response.data;

  } catch (error) {

    console.error(
      "Future Forecast API Error:",
      error
    );

    return [];
  }
};

// =====================================================
// FORECAST EVALUATION
// =====================================================

export const getForecastEvaluation = async () => {

  try {

    const response = await axios.get(
      `${BASE_URL}/api/prediction/evaluation`
    );

    return response.data;

  } catch (error) {

    console.error(
      "Forecast Evaluation API Error:",
      error
    );

    return null;
  }
};