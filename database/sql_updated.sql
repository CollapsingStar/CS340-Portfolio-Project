<html>

<head>
	<title>Edit Master Table</title>
    <link href="style.css" rel="stylesheet" type="text/css" />
</head>

<body>
    <div>
        <table border="1" cellpadding="5">
            <!-- Access data tuple passed from app.py --> 
            {% if master_table %}
			    <thead>
				    <tr>
					    <!-- Iterate through each key in the first entry to get the column name -->
                        {% for key in mt[0].keys() %}
					    
                        <!-- Create a <th> tag with the key inside of it, this will be our header row -->
					    <th scope="col" data-field="{{ key }}" data-filter-control="input">{{ key }}</th>
					
                        <!-- End of this for loop -->
                        {% endfor %} 
                    </tr>

				<tbody>
					<!-- Now, iterate through every item in data -->{% for table in master_table %}
					    <tr>
						    <!-- Then iterate through every key in the current item dictionary -->
                            {% for key in table.keys() %}

						    <!-- Create a <td> element with the value of that key in it -->
						    <td> {{table[key]}} </td> 
                            {% endfor %}
					    </tr> 
                        {% endfor %} 
            {% endif %} 
        </table>   

        <div id="update">
            <!-- form to edit data in bsg_people-->
            <form id="updateOrder" action="/edit_table/{{data[0].table_id}}" method="post">
                <legend><strong>Edit Master Table</strong></legend>
                <fieldset>
                    <input type="hidden" value="{{data[0].table_id}}" class="form-control" id="table_id" name="table_id" required>

                    <label for="total_guests">Total Guests</label>
                    <input type="text" value="{{data[0].total_guests}}" class="form-control" id="total_guests" name="total_guests" pattern="{1-9}" required>

                    <label for="total_riders">Total Riders</label>
                    <input type="text" value="{{data[0].total_riders}}" class="form-control" id="total_riders" name="total_riders" pattern="{1-9}">

                    <label for="date">Date:</label>
                    <input type="text" value="{{data[0].date}}" class="form-control" id="date" name="date">

                </fieldset>
                <input type="submit" value="Save Master Table" name="edit_table" class="btn btn-primary" style="margin:.5rem;">
                <a href='/master_table'><input class="btn" type="button" value="cancel"></a>
            </form>

</html>