# Datadog Meta-Buildpack

This is a Cloud Foundry decorator, unlike a "real" buildpack, a decorator doesn't produce a droplet from source. Instead, it "decorates" (hence the name) an already produced droplet to implement some kind of add-on feature.

This decorator injects Datadog environment variables inside the droplet.

For more information on the available environment variables: 

https://docs.datadoghq.com/tracing/setup_overview/setup/java/?tab=otherenvironments