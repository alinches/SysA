import json

def membership_function(points, x):
    if x <= points[0][0]:
        return points[0][1]
    if x >= points[-1][0]:
        return points[-1][1]
    for i in range(len(points)-1):
        x1, mu1 = points[i]
        x2, mu2 = points[i+1]
        if x1 <= x <= x2:
            if x2 == x1:
                return mu1
            return mu1 + (mu2 - mu1)*(x - x1)/(x2 - x1)
    return 0.0  

def build_membership_functions(json_str):
    data = json.loads(json_str)
    var_name = list(data.keys())[0]
    terms = {}
    for term in data[var_name]:
        pts = sorted(term["points"], key=lambda p: p[0])
        terms[term["id"]] = pts
    return terms

def aggregate_output_terms(terms, resolution=100):
    all_x = []
    for pts, mu_level in terms:
        all_x.extend([p[0] for p in pts])
    min_x = min(all_x)
    max_x = max(all_x)
    step = (max_x - min_x) / (resolution - 1) if resolution > 1 else 1
    
    max_mu_for_x = []
    for i in range(resolution):
        xv = min_x + i*step
        mus = []
        for pts, mu_level in terms:
            base_mu = membership_function(pts, xv)
            mus.append(min(base_mu, mu_level))
        max_mu_for_x.append((xv, max(mus) if mus else 0.0))
    return max_mu_for_x

def defuzzify_first_max(membership_profile):
    max_mu = max(mu for x, mu in membership_profile)
    for x, mu in membership_profile:
        if mu == max_mu:
            return x
    return membership_profile[0][0]  

def task(temp_json_str: str, heat_json_str: str, rules_json_str: str, current_temp: float) -> float:
    temp_terms = build_membership_functions(temp_json_str)
    temp_memberships = {term: membership_function(temp_terms[term], current_temp) for term in temp_terms}
    
    heat_terms = build_membership_functions(heat_json_str)
    
    rules = json.loads(rules_json_str)
    
    activated_terms = []
    for rule in rules:
        input_term, output_term = rule
        mu_input = temp_memberships.get(input_term, 0.0)
        if output_term in heat_terms:
            activated_terms.append((heat_terms[output_term], mu_input))
    
    if not activated_terms:
        return 0.0
    
    aggregated_profile = aggregate_output_terms(activated_terms)
    
    result = defuzzify_first_max(aggregated_profile)
    return result

if __name__ == "__main__":
    temp_json_str = json.dumps({
        "температура": [
            {"id": "холодно", "points": [[0,1],[18,1],[22,0],[50,0]]},
            {"id": "комфортно", "points": [[18,0],[22,1],[24,1],[26,0]]},
            {"id": "жарко", "points": [[0,0],[24,0],[26,1],[50,1]]}
        ]
    }, ensure_ascii=False)

    heat_json_str = json.dumps({
        "температура": [
            {"id": "слабый", "points": [[0,0],[0,1],[5,1],[8,0]]},
            {"id": "умеренный", "points": [[5,0],[8,1],[13,1],[16,0]]},
            {"id": "интенсивный", "points": [[13,0],[18,1],[23,1],[26,0]]}
        ]
    }, ensure_ascii=False)

    rules_json_str = json.dumps([
        ["холодно", "интенсивный"],
        ["комфортно", "умеренный"],
        ["жарко", "слабый"]
    ], ensure_ascii=False)

    current_temp = 20.0
    print(task(temp_json_str, heat_json_str, rules_json_str, current_temp))

