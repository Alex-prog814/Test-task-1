  const data = departmentTreeData;
  const width = 1500;
  const marginTop = 10;
  const marginRight = 10;
  const marginBottom = 10;
  const marginLeft = 40;

  const root = d3.hierarchy(data);
  const dx = 20;
  const dy = (width - marginRight - marginLeft) / (1 + root.height);

  const tree = d3.tree().nodeSize([dx, dy]);
  const diagonal = d3.linkHorizontal().x(d => d.y).y(d => d.x);

  const svg = d3.create("svg")
      .attr("width", '100%')
      .attr("height", dy)
      .attr("viewBox", [-marginLeft, -marginTop, width, dy])
      .attr("style", "font: 10px sans-serif; user-select: none; margin-bottom: 5%;");

  const gLink = svg.append("g")
      .attr("fill", "none")
      .attr("stroke", "#555")
      .attr("stroke-opacity", 0.4)
      .attr("stroke-width", 1.5);

  const gNode = svg.append("g")
      .attr("cursor", "pointer")
      .attr("pointer-events", "all");

  function update(event, source) {
    const duration = event?.altKey ? 2500 : 250;
    const nodes = root.descendants().reverse();
    const links = root.links();

    tree(root);

    let left = root;
    let right = root;
    root.eachBefore(node => {
      if (node.x < left.x) left = node;
      if (node.x > right.x) right = node;
    });

    const height = right.x - left.x + marginTop + marginBottom;

    const transition = svg.transition()
        .duration(duration)
        .attr("height", height)
        .attr("viewBox", [-marginLeft, left.x - marginTop, width, height])
        .tween("resize", window.ResizeObserver ? null : () => () => svg.dispatch("toggle"));

    const node = gNode.selectAll("g")
      .data(nodes, d => d.id);

    const nodeEnter = node.enter().append("g")
        .attr("transform", d => `translate(${source.y0},${source.x0})`)
        .attr("fill-opacity", 0)
        .attr("stroke-opacity", 0)

    nodeEnter.append("circle")
        .attr("r", 4.5)
        .attr("fill", d => d._children ? "#555" : "#999")
        .attr("stroke-width", 10)
        .on("click", (event, d) => {
          d.children = d.children ? null : d._children;
          update(event, d);
        });

    nodeEnter.append("text")
        .attr("dy", "1em")
        .attr("x", d => d._children ? -6 : 6)
        .attr("id", d => d.data.id)
        .attr("text-anchor", d => d._children ? "end" : "start")
        .text(d => d.data.name)
        .on('click', (e) => {
            if(e.target.innerHTML === 'Root') return;
            window.location.href = `/departments-tree/${e.target.id}/`
        })
      .clone(true).lower()
        .attr("stroke-linejoin", "round")
        .attr("stroke-width", 3)
        .attr("stroke", "white");

    const nodeUpdate = node.merge(nodeEnter).transition(transition)
        .attr("transform", d => `translate(${d.y},${d.x})`)
        .attr("fill-opacity", 1)
        .attr("stroke-opacity", 1);

    const nodeExit = node.exit().transition(transition).remove()
        .attr("transform", d => `translate(${source.y},${source.x})`)
        .attr("fill-opacity", 0)
        .attr("stroke-opacity", 0);

    const link = gLink.selectAll("path")
      .data(links, d => d.target.id);

    const linkEnter = link.enter().append("path")
        .attr("d", d => {
          const o = {x: source.x0, y: source.y0};
          return diagonal({source: o, target: o});
        });

    link.merge(linkEnter).transition(transition)
        .attr("d", diagonal);

    link.exit().transition(transition).remove()
        .attr("d", d => {
          const o = {x: source.x, y: source.y};
          return diagonal({source: o, target: o});
        });

    root.eachBefore(d => {
      d.x0 = d.x;
      d.y0 = d.y;
    });
  }

  root.x0 = dy / 2;
  root.y0 = 0;
  root.descendants().forEach((d, i) => {
    d.id = i;
    d._children = d.children;
    if (d.depth && d.data.name.length !== 7) d.children = null;
  });

  update(null, root);

  const svgContainer = document.getElementById('svg-block');
  svgContainer.appendChild(svg.node());
