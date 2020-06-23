//! Python was annoying me so I wrote the post parser in rust

use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

#[pymodule]
fn blog(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pyfunction!(title)).unwrap();
    m.add_wrapped(wrap_pyfunction!(date)).unwrap();
    m.add_wrapped(wrap_pyfunction!(description)).unwrap();
    Ok(())
}


/// Extract first line to use as title
#[pyfunction]
pub fn title(content: &str) -> Option<String> {
    content
        .lines()
        .filter(|s| s.starts_with("#"))
        .next()
        .and_then(|s| s.strip_prefix("# "))
        .map(|s| s.chars().filter(|c| &c.to_string() != "\\").collect::<String>())
}

/// Extract the first line beginning with a * to be used as the date
#[pyfunction]
pub fn date(content: &str) -> Option<String> {
    content
        .lines()
        .filter(|s| s.starts_with("*"))
        .next()
        .and_then(|s| s.strip_prefix("*"))
        .and_then(|s| s.strip_suffix("*"))
        .map(|s| s.to_string())
}

/// Extract the first paragraph for the description
#[pyfunction]
pub fn description(content: &str) -> Option<String> {
    content
        .lines()
        .skip_while(|s| {
            s.starts_with("#") | s.starts_with("*") | { s == &"" }
        })
        .collect::<Vec<&str>>()
        .split(|s| s == &"")
        .next()
        .map(|s| s.join(" "))
}
