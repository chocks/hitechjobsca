import React, { Component } from 'react';



class Loading extends Component {
    render() {
        let styles = {
            border: 0,
            width: '150px',
            height: '150px'
        };
        return (
            <li className="list-group-item" key="loading">
            <div className="card bg-light float-center">
                <div className="card-header">
                    <p>Loading...</p>
                    <img className="float-center" src="/static/loading.gif" style={styles} alt="Loading..." />
                </div>
            </div>
    </li>
        );
    }
}

export default Loading;
