from app.services.feature_extraction import EngineeredFeatures


def test_engineered_features_counts():
    text = "Urgent! Click https://1.2.3.4/login now. Reply-To: test"
    features = EngineeredFeatures().transform([text])[0]
    keyword_freq, url_count, ip_url_count, _, _, header_anomaly = features

    assert url_count >= 1
    assert ip_url_count >= 1
    assert header_anomaly == 1
    assert keyword_freq > 0
