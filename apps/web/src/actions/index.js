import axios from 'axios';

// Same-origin: nginx (apps/web/nginx.conf) reverse-proxies the API paths to
// the `api` service, so requests resolve to `/ca_jobs`, `/new`, `/search`.
const API = '';

export const FETCH_JOBS = 'fetch_jobs';
export const CREATE_JOB = "create_job";
export const SEARCH_JOBS = "search_job";

export function fetchJobs() {
    const request = axios.get(`${API}/ca_jobs`);

    return {
        type: FETCH_JOBS,
        payload: request
    };
}


export function createJob(values, callback) {
    const request = axios.post(`${API}/new`, values)
        .then(() => callback());
    
    return {
        type: CREATE_JOB,
        payload: request
    };
}

export function searchJobs(searchString) {
    const request = axios.get(`${API}/search?searchString=${searchString}`);

    return {
        type: SEARCH_JOBS,
        payload: request
    };
}