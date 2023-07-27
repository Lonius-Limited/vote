import { Authorization, FetchWrapper } from "../lib/auth"
import { getCookie } from "../lib/cookies";
import {
  useFrappePostCall,
} from "frappe-react-sdk";

export const _defaultHeaders = {
  "Content-Type": "application/json",
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "X-Requested-With",
  Authorization
};

export const sendOTPtoVoter = async () => {

  return {}


}


