import React from "react";

import CategoryBreakdownTable
  from "./CategoryBreakdownTable";

import "../css/CategoryBreakdownModal.css";

const CategoryBreakdownModal = ({
  isOpen,
  month,
  data,
  onClose
}) => {

  if (!isOpen) {
    return null;
  }

  return (

    <div className="modal-overlay">

      <div className="modal-container">

        <div className="modal-header">

          <h2>
            Category Workforce Breakdown - {month}
          </h2>

          <button
            className="close-btn"
            onClick={onClose}
          >
            ✕
          </button>

        </div>

        <div className="modal-body">

          <CategoryBreakdownTable

            hideHeader={true}

            data={[
              {
                month,
                workloadBreakdown: data
              }
            ]}

          />

        </div>

      </div>

    </div>

  );

};

export default CategoryBreakdownModal;