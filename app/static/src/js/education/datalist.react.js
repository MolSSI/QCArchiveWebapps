import React, { Component } from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';

const propTypes = {

	id: PropTypes.string,

	style: PropTypes.object
};

const defaultProps = {
	id : 'molecular',
};

class datalist extends Component {

	render(){
		var mydata = require('../../../mymap.json');
		var op = [];
		op = mydata.map(item => {
			return <option value={item.name} />
		});

		const { id } = this.props;
		return(
			<datalist id={id}>
				{op}
			</datalist>
		)
		
	}


}

datalist.propTypes = propTypes
datalist.defaultProps = defaultProps;
export default datalist;