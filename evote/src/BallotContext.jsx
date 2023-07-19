import React, { createContext, useState } from "react";

const BallotContext = createContext();

const BallotProvider = ({ children }) => {
  //States
  const [voterInfo, setVoterInfo] = useState(null);
  const [ballotData, setBallotData] = useState(null);
  const [ballotReceipt, setBallotReceipt] = useState([]);
  const [hasVoted, setHasVoted] = useState(false);
  const [ballotLength, setBallotLength] = useState(0);
  //Functions
  const updateVoterInfo = ({ bioData }) => {
    /*{
        "institution": "MTRH Staff Pension Scheme",
        "institution_contact": null,
        "voter_name": "SELINA, O. MWANGU",
        "is_official": 0,
        "county_facility": "MTRHSPS STATION",
        "voter_branch": "MTRH Staff Pension Scheme",
        "voter_phone": "722810063",
        "voter_email": "selinamwangu@mtrh.go.ke",
        "member_id": "2063",
        "board_number": null,
        "id_number": "2063",
        "election": "EL-MTRH Staff Pension Scheme-2022-12257",
        "election_start": "2022-02-04 06:00:00",
        "election_ends": "2022-02-04 07:45:00",
        "status": "Closed",
        "in_register": 1,
        "has_voted": "No"
    }*/
    setVoterInfo((currVal) => bioData);
  };

  const addToBallotReceipt = ({ ballotSelection }) => {
    const positionExists =
      ballotReceipt.find((x) => x.position === ballotSelection.position) ||
      null;

    if (!positionExists) {
      setBallotReceipt([...ballotReceipt, ballotSelection]);

      return;
    }
    const maximumPositions = positionExists.maximum_number_of_positions;
    const alreadySelected = positionExists.candidates.length || 1;
    if (maximumPositions < alreadySelected + 1) {
        return new Error(`Sorry, you cannot select more than ${maximumPositions} candidates for ${ballotSelection.position}`)
    }

    ballotReceipt
      .find((x) => x.position === choice.position)
      .candidates.map((r) => (r.choice = 7));

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
  };
  const setVoteStatus = ({ val }) => {
    setHasVoted((currVal) => val);
  };

  return (
    <BallotContext.Provider
      value={{
        voterInfo,
        updateVoterInfo,
        ballotData,
        updateBallot,
        ballotReceipt,
        updateBallotReceipt: addToBallotReceipt,
        hasVoted,
      }}
    >
      {children}
    </BallotContext.Provider>
  );
};
export default BallotContext;
