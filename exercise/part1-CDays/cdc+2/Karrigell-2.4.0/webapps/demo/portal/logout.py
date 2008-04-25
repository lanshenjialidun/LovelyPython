# logout by setting user attribute to None

so=Session()
so.user=None

raise HTTP_REDIRECTION,"index.pih"