import _ from 'lodash';
import React, { Component } from 'react';
import { connect } from 'react-redux';
import { fetchJobs, searchJobs } from '../actions';
import moment from 'moment';

 
class JobSearch extends Component {
    constructor(props) {
        super(props);
        this.textInput = React.createRef();
        this.onChange = this.onChange.bind(this);
        this.showLog = this.showLog.bind(this);
    }

    onChange(event) {
        this.textInput.current.focus();
        if (event.key === 'Enter') {
            this.props.searchJobs(event.target.value);
        } 
    }

    showLog(event) {
        this.textInput.current.focus();
        this.props.searchJobs(this.textInput.current.value);
    }

    allJobs() {
        this.textInput.current.value = '';
        this.props.fetchJobs();
    }

    render() {
        let styles = {
            paddingTop: '10px',
            paddingBottom: '10px'
        };
        return (
            <div className="input-group mb-2">
                <input type="text" className="form-control" 
                        placeholder="Search.. ex: Java developer in Toronto" 
                        aria-label="Search.."
                        aria-describedby="basic-addon2" 
                        onKeyPress={this.onChange.bind(this)}
                        ref={this.textInput}
                />
                <div className="input-group-append">
                    <button className="input-group-text btn-primary" onClick={this.showLog.bind(this)}>
                        <i className="material-icons">search</i>
                    </button>
                </div>
                <div className="input-group-append">
                    <button className="input-group-text btn-primary" onClick={this.allJobs.bind(this)}>
                        <i className="material-icons">clear</i>
                    </button>
                </div>
            </div>
        );
    }
}

function mapStateToProps(state) {
    return { searchString: state.searchString };
}

export default connect(mapStateToProps, { fetchJobs, searchJobs })(JobSearch);