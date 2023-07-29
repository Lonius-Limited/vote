import React, { createContext, useState } from "react";

const BallotContext = createContext();

export const BallotProvider = ({ children }) => {
  //States
  const [ballotData, setBallotData] = useState(null);
  //Functions

  const updateBallotData = (voterChoice) => {
    
  };
  const createBallotData = (ballotRcpt)=>{
    setBallotData(r=>ballotRcpt)
  }

  return (
    <BallotContext.Provider
      value={{
        ballotData,
        updateBallotData,
        createBallotData
      }}
    >
      {children}
    </BallotContext.Provider>
  );
};
export default BallotContext;

/*
    {
                "position": "MTRH Pension Trustee",
                "branch": "MTRHSPS STATION",
                "maximum_number_of_positions": 1,
                "candidates": [
                    {
                        "candidate_id": "MTRHSPS/MTRHSPS/V0012256",
                        "candidate_name": "TEST, CANDIDATE",
                        "political_party": null,
                        "party_symbol": null,
                        "headshot": "https://elections.erpnextkenya.com",
                        "choice": 0
                    }
                ]
            }
    */