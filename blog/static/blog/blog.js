class PostRow extends React.Component {
  render() {
    const post = this.props.post;
    let thumbnail;
    if (post.hero_image.thumbnail) {
      thumbnail = <img src="post.hero_image.thumbnail"/>
    } else {
      thumbnail = "-"
    }

    return <tr>
            <td>{post.title}</td>
            <td>{thumbnail}</td>
            <td>{post.tags.join(", ")}</td>
            <td>{post.slug}</td>
            <td>{post.summary}</td>
            <td>
              <a href={"/posts/" + post.slug + "/"}>View</a>
            </td>
          </tr>
  }
}

class PostTable extends React.Component {
  state = {
    dataLoaded: false,
    data: {
      results: [
        {
          id: 1,
          tags: [
              'django', 'react'
            ],
          hero_image: {
            'thumbnail': '/media/__sized__/hero_images/snake-419043_1920-thumbnail-100x100-70.jpg',
            'full_size': '/media/hero_images/snake-419043_1920.jpg'
          },
          title: 'Test Post',
          slug: 'test-post',
          summary: 'A test post, created for Django/React.'
        }
      ]
    }
  }
  
  render() {
    let rows;
    if (this.state.dataLoaded) {
        if (this.state.data.results.length > 0) {
          rows = this.state.data.results.map(value => <PostRow post={value}/>)
        } else {
          rows = <tr><td colSpan="6">No posts were found.</td></tr>
        }
    } else {
      rows = <tr><td colSpan="6">Loading&hellip;</td></tr>
    }
    return <table className="table table-striped table-bordered mt-2">
            <thead>
              <tr>
                <th>Title</th>
                <th>Image</th>
                <th>Tags</th>
                <th>Slug</th>
                <th>Summary</th>
                <th>Link</th>
              </tr>
            </thead>
            <tbody>
              {rows}
            </tbody>
          </table>
  }
}

const domContainer = document.getElementById("react_root");
ReactDOM.render(
  React.createElement(PostTable), 
  domContainer
);
