from flask import Flask, render_template, request
import json
import numpy as np

# from curvature import (
#     node_resistance_curvature,
#     link_resistance_curvature,
#     foster_coefficients,
# )

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "POST":
        return render_template("index.html")
    return render_template("index.html")

@app.route("/get-labels", methods=["POST"])
def get_labels():
    print("request.form:", request.form)
    user_data = request.form
    try:
        LM = json.loads(user_data['lm'])  # laplacian matrix
        V = json.loads(user_data['v'])
        t = json.loads(user_data['t'])
        print("Type =", t)
    except Exception as e:
        print("error triggered:", e)
        return '["error0"]'

    # calculate number of spanning trees
    LMred = np.matrix(LM)
    LMred = LMred[:-1, :-1]
    kappa = np.linalg.det(LMred)
    kappa = int(np.round(kappa))
    print("sp tree count:", kappa)

    print("get-labels success")
    # return json.dumps(kappa)

    if t == 1:
        # link resistance curvature
        try:
            # LRC = link_resistance_curvature(LM)
            ret = dict()
            ret["LM"] = LM
            ret["LRC"] = [[0 for _ in range(len(V))] for _ in range(len(V))]
            ret["kappa"] = kappa

            # for i in range(len(V)):
            #     for j in range(len(V)):
            #         ret["LRC"][i][j] = round(LRC[i][j], 3)
        except Exception as e:
            print("error:", e)
            return '["error19"]'
    else:
        print(f"error: type t={t} not recognized")
        return "error"
    return json.dumps(ret)

    # return (
    #     json.dumps({"success": True}),
    #     200,
    #     {"ContentType": "application/json"}
    # )

if __name__ == "__main__":
    app.run(debug=True)