from flask import Flask, render_template, request
import json
# import matplotlib.pyplot as plt
# import matplotlib as mpl

from resistance import (
#     node_resistance_curvature,
#     link_resistance_curvature,
    foster_coefficients,
    spanning_tree_count,
    two_forest_count,
    tau_constant,
)

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
    kappa = spanning_tree_count(LM)
    kappa2 = two_forest_count(LM)
    tau = tau_constant(LM)
    print("tau_const:", tau)

    print("get-labels success")
    # return json.dumps(kappa)

    if t == 1:
        # link resistance curvature
        try:
            FC = foster_coefficients(LM)
            ret = dict()
            ret["LM"] = LM
            ret["FC"] = [[0 for _ in range(len(V))] for _ in range(len(V))]
            ret["edgeColor"] = [[0 for _ in range(len(V))] for _ in range(len(V))]
            ret["kappa"] = kappa
            ret["kappa2"] = kappa2
            ret["tau"] = tau

            # cmap = mpl.colormaps['Blues']
            for i in range(len(V)):
                for j in range(len(V)):
                    ret["FC"][i][j] = round(FC[i][j], 3)
                    # ret["edgeColor"] = cmap(FC[i][j])
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