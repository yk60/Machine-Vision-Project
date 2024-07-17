from matrix import DigitMatrix
def generate_html_table(DigitMatrix):
    imgs = (list(DigitMatrix.img_dict.keys()))
    # Opening HTML structure
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cosine Similarity Results</title>
        <style>
            table {
                width: 100%;
                border-collapse: collapse;
            }
            table, th, td {
                border: 1px solid black;
            }
            th, td {
                padding: 10px;
                text-align: center;
            }
            img {
                max-width: 100px;
                height: auto;
            }
        </style>
    </head>
    <body>
        <h1>Cosine Similarity Results</h1>
        <table>
            <thead>

            </thead>
            <tbody>
    """
    
    # Iterate through cosine similarity matrix to populate table rows

    html_content += "<tr>"
    html_content += "<td>""</td>"
    for img in imgs:
        html_content += f'<td><img src="{DigitMatrix.path}/{img}" alt="Image"></td>'
    html_content += "</tr>"
    i = 0
    for row in DigitMatrix.cos_similarity:
        html_content += "<tr>"
        html_content += f'<th scope="row"><img src="{DigitMatrix.path}/{imgs[i]}" alt="Image"></th>\n'
        for entry in row:
            html_content += f"<td>{entry}</td>"
        html_content += "</tr>"
        i+=1
            
    # Closing HTML structure
    html_content += """
            </tbody>
        </table>
    </body>
    </html>
    """
    with open('index.html', 'w') as html_file:
        html_file.write(html_content)

    return html_content  # Return HTML content as string if needed
