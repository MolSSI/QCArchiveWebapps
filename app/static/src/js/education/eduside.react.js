import React, { Component } from 'react';
import classNames from 'classnames';
import PropTypes from 'prop-types';
import DataTable from 'react-data-table-component';

const propTypes = {

	id: PropTypes.string,

	style: PropTypes.object
};

const defaultProps = {
	id : 'orb',
};


class eduside extends Component{
    constructor(props) {
        super(props);
        this.state = {
            loading: 
            <div style={{marginTop: '50px'}}>
                <div className="row justify-content-md-center" style={{marginTop: '20px', fontSize: '15px'}}>
                    <div className="col">
                    <button className="btn btn-light btn-block" id='orb' onClick={(e) => this.changeSide(e, "Orbitals")}>Orbitals</button>
                    </div>
                </div>
                <div className="row justify-content-md-center" style={{marginTop: '20px', fontSize: '15px'}}>
                    <div className="col">
                    <button className="btn btn-light btn-block" id='dip' onClick={(e) => this.changeSide(e, "Dipoles")}>Dipoles</button>
                    </div>
                </div>
                <div className="row justify-content-md-center" style={{marginTop: '20px', fontSize: '15px'}}>
                    <div className="col">
                    <button className="btn btn-light btn-block" id='vib' onClick={(e) => this.changeSide(e, "Vibration")}>Vibration</button>
                    </div>
                </div>
                <div className="row justify-content-md-center" style={{marginTop: '20px', fontSize: '15px'}}>
                    <div className="col">
                    <button className="btn btn-light btn-block" id='rot' onClick={(e) => this.changeSide(e, "Rotation")}>Rotation</button>
                    </div>
                </div>
            </div>,
            
            
        };
        this.data = [
            {
                id: 0,
                catename: 1,
                symmetry: 'A1',
                occupancy: 2,
                energy: -20.55,
                show: false
            },
            {
                id: 1,
                catename: 1,
                symmetry: 'A1',
                occupancy: 2,
                energy: -22.55,
                show: false
              
            },
            {
                id: 2,
                catename: 1,
                symmetry: 'A1',
                occupancy: 2,
                energy: -22.55,
                show: false
               
            },
            {
                id: 3,
                catename: 1,
                symmetry: 'A1',
                occupancy: 2,
                energy: -22.55,
                show: false

            },
            {
                id: 4,
                catename: 1,
                symmetry: 'A1',
                occupancy: 2,
                energy: -22.55,
                show: false

            },

        ];
        this.changeSide = this.changeSide.bind(this);
        this.returnSide = this.returnSide.bind(this);
        //this.showView = this.showView.bind(this);
    }

    
    changeSide(e, category) {

        const columns = [
            // { cell: () => <input type="radio" onClick={handleClick}></input>},
            { name: category, selector: 'catename' },
            { name: 'Symmetry', selector: 'symmetry' },
            { name: 'Occupancy', selector: 'occupancy' },
            { name: 'Energy', selector: 'energy' },
            // { name: '', selector: 'show' },
          ];



        // const handleChange = (state) => {
        //     // You can use setState or dispatch with something like Redux so we can use the retrieved data
        //     console.log('Selected Rows: ', state); 
        //     if (state.selectedCount != 0) {
        //         this.data.forEach((row) => row.show = true); 
        //         this.data[state.selectedRows[0].id].show = false;  
        //     } else {
        //         this.data.forEach(row => row.show = false);
        //     }
            
        //     this.data.forEach(row => console.log(row.show));
        //     this.changeSide(e, category);
        // };

        const handleClick = (state) => {
            console.log('click row: ', state);
        }

        const table = (
                <div className="container-fluid pr-0">
                    <div className="row">
                        <div className="col">
                            <button className="btn btn-info" style={{float: 'left', width: '60px', marginTop: '10px'}} 
                            onClick={(e) => this.returnSide(e)}><strong>Back</strong></button>
                        </div>
                        {/* <div className="col">
                            <button className="btn btn-info" style={{float: 'right', width: '60px'}}
                            onClick={(e) => this.showView(e)}>View</button>
                        </div> */}
                    </div>
                    <div className="row">
                        <div className="col">
                        <DataTable
                            title= {category}
                            columns={columns}
                            data={this.data}
                            onRowClicked={handleClick}
                            highlightOnHover
                            pointerOnHover
                            // selectableRows
                            // selectableRowsNoSelectAll
                            // onRowSelected={handleChange}
                            // selectableRowsDisabledField="show"                       
                        />
                        </div>
                    </div>
                </div>
        );
      
        this.setState({
            loading: table
        })
    }

    returnSide(e) {
        const intialSide = (
            <div style={{marginTop: '50px'}}>
                <div className="row justify-content-md-center" style={{marginTop: '20px', fontSize: '15px'}}>
                    <div className="col">
                    <button className="btn btn-light btn-block" id='orb' onClick={(e) => this.changeSide(e, "Orbitals")}>Orbitals</button>
                    </div>
                </div>
                <div className="row justify-content-md-center" style={{marginTop: '20px', fontSize: '15px'}}>
                    <div className="col">
                    <button className="btn btn-light btn-block" id='dip' onClick={(e) => this.changeSide(e, "Dipoles")}>Dipoles</button>
                    </div>
                </div>
                <div className="row justify-content-md-center" style={{marginTop: '20px', fontSize: '15px'}}>
                    <div className="col">
                    <button className="btn btn-light btn-block" id='vib' onClick={(e) => this.changeSide(e, "Vibration")}>Vibration</button>
                    </div>
                </div>
                <div className="row justify-content-md-center" style={{marginTop: '20px', fontSize: '15px'}}>
                    <div className="col">
                    <button className="btn btn-light btn-block" id='rot' onClick={(e) => this.changeSide(e, "Rotation")}>Rotation</button>
                    </div>
                </div>
            </div>
        );
        this.setState({
            loading: intialSide
        })
    }

    render() {

        
        return (
            <div>
                {this.state.loading}
            </div>
        )
    }
}

eduside.propTypes = propTypes
eduside.defaultProps = defaultProps;
export default eduside;