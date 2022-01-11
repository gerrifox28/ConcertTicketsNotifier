import './App.css';
import React, { useState } from 'react';

const App = () => {

  const [event, setEvent] = useState();
  const [date, setDate] = useState();
  const [city, setCity] = useState();
  const [url, setUrl] = useState();
  const [resultNum, setResultNum] = useState(0);
  const [correctUrl, setCorrectUrl] = useState(false);
  const [section, setSection] = useState();
  const [row, setRow] = useState();
  const [numTickets, setNumTickets] = useState();
  const [price, setPrice] = useState('');
  const [all, setAll] = useState(true);
  const [openUrl, setOpenUrl] = useState(false);
  const [disabledUrl, setDisabledUrl] = useState(true);
  const [disabledTicket, setDisabledTicket] = useState(true);
  const [urlList, setUrlList] = useState();

  const handleEventChange = (input) => {
   setEvent(input.target.value);
   if (input.target.value) setDisabledUrl(false);
   else if(!date && !city) setDisabledUrl(true);
  }

  const handleDateChange = (input) => {
    setDate(input.target.value);
    if (input.target.value) setDisabledUrl(false);
    else if(!event && !city) setDisabledUrl(true);
   }

   const handleCityChange = (input) => {
    setCity(input.target.value);
    if (input.target.value) setDisabledUrl(false);
    else if(!event && !date) setDisabledUrl(true);
   }

   const handleSectionChange = (event) => {
    setSection(event.target.value);
    setDisabledTicket(false)
   }

   const handleRowChange = (event) => {
    setRow(event.target.value);
    setDisabledTicket(false)
   }

   const handleNumTicketsChange = (event) => {
    setNumTickets(event.target.value);
    setDisabledTicket(false)
   }

   const handlePriceChange = (event) => {
    setPrice(event.target.value.replace('$', ''));
    setDisabledTicket(false)
    
   }

   const handleAllChange = (event) => {
    setAll(event.target.value);
   }

   const handleOpenUrlChange = (event) => {
    setOpenUrl(event.target.value);
   }

  const handleSubmitUrlSearch = (input) => {
    if (event && date && city) {
      alert('Event info was submitted: ' + event + ', ' + date + ', ' + city);
      input && input.preventDefault();
      //send request to search for url
      setUrl("https://www.stubhub.com/olivia-rodrigo-new-york-tickets-4-26-2022/event/105133478/")
    } else {
      alert('Please input all search fields and resubmit')
      input.preventDefault();
    }
  }

  const handleSubmitTicketSearch = (input) => {
    //send request to search for tickets
    alert('Ticket info was submitted: ' + section + ', ' + row + ', ' + numTickets + ', ' + price + ', ' + all + ', ' + openUrl);
    input.preventDefault();
    //setmatchesurllist from response
    setUrlList('http, https, .com')
  }

  return (
    <div className="App">
      <form onSubmit={handleSubmitUrlSearch}>
        <label>
          Event:
          <input type="text" value={event} defaultValue={event || ''} onChange={handleEventChange} />
        </label>
        <label>
          Date:
          <input type="text" value={date} defaultValue={date || ''} onChange={handleDateChange} />
        </label>
        <label>
          City:
          <input type="text" value={city} defaultValue={city || ''} onChange={handleCityChange} />
        </label>
        <input type="submit" value="Submit" disabled={disabledUrl}/>
      </form>
    {url && 
      <div>Is this the event you are looking for? {url}
      <button onClick={() => setCorrectUrl(true)}>Yes</button>
      <button onClick={() => {
        setResultNum(resultNum+1);
        setUrl('');
        console.log(url);
        <div>Retrieving next Url</div>
        handleSubmitUrlSearch()
        console.log(url);
        //recall handleSubmit to get new url
      }}>No</button>
      </div>}
      {correctUrl && 
      <div> 
        <form onSubmit={handleSubmitTicketSearch}>
        <label>
          Section:
          <input type="text" value={section} defaultValue={section || ''} onChange={handleSectionChange} />
        </label>
        <label>
          Row:
          <input type="text" value={row} defaultValue={row || ''} onChange={handleRowChange} />
        </label>
        <label>
          Number of Tickets:
          <input type="text" value={numTickets} defaultValue={numTickets || ''} onChange={handleNumTicketsChange} />
        </label>
        <label>
         Price:
          <input type="text" value={'$' + price} defaultValue={price || '$'} onChange={handlePriceChange} />
        </label>
        <label>
          Apply all inputted filters:
          <input type="text" value={all} onChange={handleAllChange} />
        </label>
        <label>
         Open matched ticket urls:
          <input type="text" value={openUrl} onChange={handleOpenUrlChange} />
        </label>
        <input type="submit" value="Submit" disabled={disabledTicket} />
      </form>
      </div>}
    {urlList && 
      <div>Matches Found: {urlList}
      </div>}

    </div>
  );
}

export default App;
