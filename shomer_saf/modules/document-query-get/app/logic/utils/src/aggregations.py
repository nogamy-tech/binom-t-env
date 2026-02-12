from typing import Dict, Tuple, List


def aggregate_query_responses(query_docs: List[Dict]) -> Tuple[List[Dict], List[Dict], Dict[str, int]]:
    """
    Aggregate query responses from DocumentsQueryJobs.
    
    Args:
        query_docs: List of documents from DocumentsQueryJobs
        
    Returns:
        Tuple containing:
        - QueriesPageResults: List of per-page results
        - QueriesResults: List of aggregated per-query results
        - QueriesAggregatedResults: Overall aggregated statistics
    """
    import json
    
    
    # Build QueriesPageResults - results per query per page
    queries_page_results = []
    query_results_dict = {}  # queryID -> {compliance_values: [], confidence_values: []}
    
    # Process query documents - each query doc may have responses for different pages
    for query_doc in query_docs:
        
        query_id = query_doc.get("Query_number", "")
        page_num = query_doc.get("Page_number", "")

        
        # Get response data
        response_data = query_doc.get("QueryResponse", {})
        if isinstance(response_data, str):
            try:
                response_data = json.loads(response_data)
            except:  # noqa: E722
                response_data = {}
        
        # Extract compliance and confidence from response
        if isinstance(response_data, dict):
            compliance = response_data.get("final_answer", False)
            confidence = response_data.get("confidence", 0)
            response_text = response_data.get("chain_of_thought", "") or str(response_data)
        else:
            compliance = False
            confidence = 0
            response_text = str(response_data)
        
        # Normalize confidence (expect 0-100, convert to 0-1 if needed)
        if confidence > 1:
            confidence = confidence / 100.0
        
        # Add to page results
        queries_page_results.append({
            "queryID": str(query_id),
            "page": str(page_num),
            "response": response_text,
            "compliance": str(compliance),
            "confidence": str(confidence)
        })
        
        # Track for aggregation
        if query_id not in query_results_dict:
            query_results_dict[query_id] = {
                "compliance_values": [],
                "confidence_values": []
            }
        
        query_results_dict[query_id]["compliance_values"].append(compliance)
        query_results_dict[query_id]["confidence_values"].append(confidence)
    
    # Aggregate per-query results (merge across pages)
    # For each query, determine final compliance (True if any page is True)
    queries_results = []
    for query_id, query_data in query_results_dict.items():
        # Final compliance: True if any page returned True
        final_compliance = any(query_data["compliance_values"])
        queries_results.append({
            "queryID": str(query_id),
            "compliance": str(final_compliance)
        })
    
    # Calculate aggregated statistics
    total_queries = len(queries_results)
    true_queries = sum(1 for q in queries_results if q.get("compliance", "").lower() == "true")
    false_queries = total_queries - true_queries
    
    queries_aggregated_results = {
        "total_queries": total_queries,
        "true_queries": true_queries,
        "false_queries": false_queries
    }
    
    return queries_page_results, queries_results, queries_aggregated_results
