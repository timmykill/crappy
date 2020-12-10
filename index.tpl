<head>
	<style>
			table, th, td {
				border: 1px solid black;
			}
	</style>
</head>
<body>
	<h1>{{nomeEsame}} helper</h1>

	<form action="/upload" method="post" enctype="multipart/form-data">
		<p>upload soluzione</p>
		<select name="data">
		% for prova in proveList:
			<option value="{{prova["data"]}}">{{prova["data"]}}</option>

		% end
		</select><br>
		<input name="username" type="text">username</input><br>
		<input name="passwd" type="password">password</input><br>
		<input name="upload" type="file">soluzione in zip</input><br>
		<input type="submit">
	</form>
	
	<table style="width:100%">
		<tr>
			<th>Prova</th>
			<th>Soluzioni</th>
		</tr>
		  % for prova in proveList:
		    <tr>
		    <th><a href="{{prova["path"]}}">{{prova["data"]}}</a></th>
		  % for s in prova["soluz"]:
		    <th><a href="{{s["path"]}}">{{s["nome"]}}</a></th>
		  % end
		    </tr>
		  % end
		
	</table>
</body>
