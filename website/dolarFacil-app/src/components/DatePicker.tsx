import React,{useState} from 'react';
import "/src/App.css";
function DatePicker(){
  const [date,setDate]=useState();
return (
    <>
      <div className='DatePicker'>
      <h1>Escolha uma data</h1>
      <input type="date" onChange={e=>setDate(e.target.value)}/>
      </div>
      <div className="BotaoConfirma">
        <button>confirmar</button>
      </div>
    </>
  )
}

export default DatePicker;