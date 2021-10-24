<!DOCTYPE html>
<html lang="it">

<head>
    <title>{{nomeEsame}}_helper</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
        integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
</head>

<body class="py-4">
    <div class="container">
        <h1>{{nomeEsame}}_helper</h1>

        <h4>upload soluzione</h4>

        <section title="file_upload" class="rounded bg-light p-4 mb-3">
            <form action="/upload" method="post" enctype="multipart/form-data">
                <div class="form-row">
                    <div class="col-md-4 mb-3">
                        <label>Username</label>
                        <input type="text" name="username" class="form-control" placeholder="Username" required>
                    </div>

                    <div class="col-md-4 mb-3">
                        <label>Password</label>
                        <input type="password" name="passwd" class="form-control" placeholder="Password" required>
                    </div>
                    <div class="col-md-4 mb-3">
                        <label>Prova</label>
						<select name="data" class="form-control" required>
						% for prova in proveList:
							<option value="{{prova["data"]}}">{{prova["data"]}}</option>

						% end
						</select><br>
                    </div>
                </div>
                <div class="form-group">
                    <div class="custom-file">
                        <input type="file" class="custom-file-input" name="upload">
                        <label class="custom-file-label" for="customFile">Soluzione in {{formatoSoluzione}}</label>
                    </div>
                </div>
                <input type="submit" class="btn btn-primary">
            </form>
        </section>

        <section title="tab_soluz">
            <h4>lista soluzioni</h4>
            <table class="table table-striped">
                <thead>
                    <th scope="col">Prova</th>
                    <th scope="col">Soluzioni</th>
                </thead>
                % for prova in proveList:
                <tr>
                    <th>
			% for p in prova["path"]:
			<a href="{{p}}">{{prova["data"]}}</a><br>
			%end
		    </th>
                    % for s in prova["soluz"]:
                    <th><a href="{{s["path"]}}">{{s["nome"]}}</a></th>
                    % end
                </tr>
                % end
            </table>
        </section>
    </div>

    <script src="https://code.jquery.com/jquery-3.4.1.slim.min.js"
        integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n"
        crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js"
        integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo"
        crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js"
        integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6"
        crossorigin="anonymous"></script>

</body>

</html>
