import _ from 'lodash';
import { FETCH_JOBS, SEARCH_JOBS } from '../actions';


export default function(state = {}, action) {
    switch(action.type) {
        case FETCH_JOBS:
        case SEARCH_JOBS: {
            const payload = action.payload && action.payload.data ? action.payload.data : null;
            const jobs = payload ? payload.allJobs : [];
            return _.mapKeys(jobs || [], 'id');
        }
        default:
            return state;
    }
}
