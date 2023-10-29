import React,{useState} from 'react';
import "/src/App.css";
function DatePicker(){
  const [date,setDate]=useState();
return (
    <>
        <div className='DatePicker bg-black bg-gradient'>
          <h1>Insira a data</h1>
          <input type="date" className='Calendar' onChange={(e) => setDate(e.target.value)}/>
          <div className="BotaoConfirma">
            <button className="block btn btn-outline-light">confirmar</button>
          </div>
        </div>
    </>
  )
}

export default DatePicker;