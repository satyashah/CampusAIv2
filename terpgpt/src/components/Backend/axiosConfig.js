import axios from "axios";

// http://127.0.0.1:5000
export default axios.create({
    baseURL: "http://127.0.0.1:5000",
    headers: {"skip-browser-warning": "true"}
});
 